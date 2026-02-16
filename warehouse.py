import paramiko
import time
import yaml


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

switch_ip = config["switch"]["ip"]
username = config["switch"]["username"]
password = config["switch"]["password"]
enable_password = config["switch"]["enable_password"]

tftp_server = config["tftp"]["server"]
backup_file = config["tftp"]["backup_file"]


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


try:

    print(f"Conneting to {switch_ip}...")
    ssh_client.connect(hostname=switch_ip, username=username, password=password)

    remote_conn = ssh_client.invoke_shell()
    time.sleep(5)

    remote_conn.send("enable\n")
    time.sleep(5)
    remote_conn.send(f"{enable_password}\n")
    time.sleep(1)

    remote_conn.send("\n")
    time.sleep(5)
    output = remote_conn.recv(65535).decode("utf-8")
    if "#" not in output:
        raise Exception(
            "Failed to enter privileged EXEC mode.Check your enable password"
        )

    remote_conn.send(f"copy startup-config tftp://{tftp_server}/{backup_file}\n")
    time.sleep(5)

    remote_conn.send("\n")
    time.sleep(5)
    remote_conn.send("\n")
    time.sleep(5)

    output = remote_conn.recv(65535).decode("utf-8")
    print(output)

    if " bytes copied " in output:
        print("Startup configuration backup complete successfully!")

    else:
        print("Backup might have failed.Check the output above.")


except Exception as e:
    print(f"An error occurred:{e}")


finally:
    ssh_client.close()
    print("Connection closed.")

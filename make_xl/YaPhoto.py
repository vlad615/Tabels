import yadisk
from key import APL_ID, APL_SCR, YA_TOKEN


client = yadisk.Client(id=APL_ID, secret=APL_SCR, token=YA_TOKEN)
# or
# client = yadisk.Client("<application-id>", "<application-secret>", "<token>")

# You can either use the with statement or manually call client.close() later
with client:
    # Check if the token is valid
    print(client.check_token())

    # Get disk information
    print(client.get_disk_info())

    # Print files and directories at "/some/path"
    print(list(client.listdir("/Мебель/Кабинет руководителя")))

    # Upload "file_to_upload.txt" to "/destination.txt"
    # client.upload("file_to_upload.txt", "/destination.txt")
    #
    # # Same thing
    # with open("file_to_upload.txt", "rb") as f:
    #     client.upload(f, "/destination.txt")
    #
    # # Download "/some-file-to-download.txt" to "downloaded.txt"
    # client.download("/some-file-to-download.txt", "downloaded.txt")
    #
    # # Permanently remove "/file-to-remove"
    # client.remove("/file-to-remove", permanently=True)
    #
    # # Create a new directory at "/test-dir"
    # print(client.mkdir("/test-dir"))
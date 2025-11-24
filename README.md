# Cloud Security Encryptor

CloudSecEncryptor is a comprehensive Python-based security application designed to provide end-to-end file protection and secure cloud storage capabilities. The project combines advanced encryption techniques with cloud integration to ensure maximum data security.


### Features

- **File Encryption & Decryption**: Securely encrypt files at the byte level using industry-standard Fernet encryption, ensuring complete data protection before cloud storage

- **Password Protection**: Implement robust password-based security with custom passphrases to lock sensitive files and prevent unauthorized access

- **Malware Scanning**: Comprehensive security scanning to detect and identify potential malware threats within files before processing or storage

- **Exploit Vulnerability Testing**: Advanced analysis to identify potential security vulnerabilities and exploitable code patterns that could compromise system integrity

- **Google Drive Integration**: Seamless cloud storage functionality with secure upload and download capabilities, maintaining encrypted file integrity throughout the process


### Setting Up Google Drive API

To get started with CloudSecEncryptor, you'll need to set up a Google Drive API project. Begin by visiting the [Google Cloud Console](https://console.cloud.google.com/) and creating a new project using the project picker. Give your project a descriptive name and click create to initialize it.

Once your project is ready, search for "Google Drive API" in the API library and enable it for your project. Next, navigate to the "API & Services" section and select "Credentials" from the sidebar. Click on "Create Credentials" and choose "OAuth client ID" from the dropdown menu.

Before you can create an OAuth client ID, Google requires you to configure your consent screen first. Set up your application by providing an app name and your email address. For the audience type, select "External" and add your email address to the test users list.

Now you can proceed with creating the OAuth client. Choose "Desktop App" as the application type and name it "Google Drive Client" for easy identification. After creating the client, download the JSON credentials file and save it securely.

Finally, make sure to navigate to the Audience section and add your email address as a test user. This step is crucial because without it, you'll encounter authentication errors during the OAuth flow when trying to access Google Drive.



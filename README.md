# Saheli-SIH

Saheli-SIH is a multi-platform defence and alert system designed to support user safety through real-time location tracking, emergency SMS notifications, and interactive dashboards. The project leverages web, mobile, and backend technologies to provide a comprehensive solution for emergency management and rapid response.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
  - [1. Twilio & Backend Setup](#1-twilio--backend-setup)
  - [2. Web Application Setup](#2-web-application-setup)
  - [3. Flutter Mobile App Setup](#3-flutter-mobile-app-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Saheli-SIH integrates several components:
- **Web Interface**: A dashboard for monitoring alerts and visualizing user locations in real time.
- **Flutter App**: Mobile application for users to trigger alerts and share location data.
- **Backend Services**: Python module for sending SMS (Twilio), storing coordinates in Firebase, and providing APIs.

---

## Features

- **Real-Time Location Tracking**: Users' coordinates are stored in Firebase and displayed on the dashboard.
- **Emergency SMS Alerts**: Sends SMS with live location to designated contacts using Twilio.
- **Web Dashboard**: Responsive interface for real-time monitoring, alert visualization, and police dashboard for authorities.
- **Multi-Platform Support**: Built with Dart (Flutter), JavaScript/React, C++, and integrated with Firebase and Twilio APIs.

---

## Tech Stack

- **Languages**: C++, Dart (Flutter), JavaScript, HTML, Swift, CMake
- **Frameworks/Libraries**: React, Express, Flutter, Twilio API, Firebase
- **Tools**: CMake for build configuration, Flask (Python) for backend API

---

## Setup & Installation

### 1. Twilio & Backend Setup

**Requirements:**
- Python 3.x
- pip (Python package manager)
- Twilio account (for SMS)
- Firebase project (for storing coordinates)

#### a. Install Dependencies

```sh
pip install flask flask-cors twilio firebase-admin
```

#### b. Twilio Account Setup

1. Sign up at [Twilio](https://www.twilio.com/).
2. Get your **Account SID** and **Auth Token** from the Twilio Console.
3. Buy a Twilio phone number (optional but recommended for production).

#### c. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/), create a new project.
2. Go to Project Settings → Service Accounts → Generate new private key, download the JSON file.
3. Place the downloaded JSON key (e.g., `firebasekey.json`) in the backend directory.

#### d. Environment Variables

Create a `.env` file or set environment variables for:

```env
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
FIREBASE_CRED_PATH=path/to/firebasekey.json
```

#### e. Running the Backend

```sh
python twlio/main.py
```

---

### 2. Web Application Setup

**Requirements:**  
- Node.js and npm installed on your system

#### a. Install Dependencies

```sh
cd saheli web interface/client
npm install
```

#### b. Running the Development Server

```sh
npm start
```

- The app should open at [http://localhost:3000](http://localhost:3000).
- If you need to run the Express server (for API/websocket), use:

```sh
cd saheli web interface
node index.js
```
- By default, the Express server runs on port **5000**.

#### c. Deployment

To build for production:

```sh
npm run build
```
This will create an optimized build in the `build` directory.

---

### 3. Flutter Mobile App Setup

**Requirements:**
- Flutter SDK ([Install Guide](https://docs.flutter.dev/get-started/install))
- Android Studio / VS Code (recommended)
- Firebase project (same as backend)

#### a. Install Flutter Dependencies

```sh
cd saheli_flutter
flutter pub get
```

#### b. Firebase Setup for Mobile

- In `lib/main.dart`, replace `"YOUR_API_KEY"`, `"YOUR_AUTH_DOMAIN"`, etc. with your actual Firebase project credentials (find these in Firebase Console → Project Settings → General).

#### c. Running the App

To run on a connected device or emulator:

```sh
flutter run
```

You can select your target device in Android Studio or with:

```sh
flutter devices
```

---

## Usage

- **Trigger SOS**: Use the Flutter app to send an SOS alert, which shares your location via SMS (using Twilio) and updates the dashboard (via Firebase).
- **Monitor Alerts**: Open the web dashboard to view real-time alerts and user locations.
- **Authorities**: Police or emergency responders can use the dashboard for rapid response and resource allocation.

---

## Contributing

Contributions are welcome! Please fork the repository, create a new branch for your changes, and submit a pull request.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Help & Resources

- [Twilio SMS Quickstart](https://www.twilio.com/docs/sms/send-messages)
- [Firebase Admin SDK Docs](https://firebase.google.com/docs/admin/setup)
- [Flutter Get Started](https://docs.flutter.dev/get-started/install)
- [React Getting Started](https://react.dev/learn)

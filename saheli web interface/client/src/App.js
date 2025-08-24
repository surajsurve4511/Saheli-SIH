import React, { useEffect, useState } from "react";
import MapComponent from './MapComponent';
import { initializeApp } from "firebase/app";
import { getFirestore, onSnapshot, collection, query, orderBy, limit } from "firebase/firestore";
import './App.css';

function App() {
  const [alertMessage, setAlertMessage] = useState("");
  const [coordinates] = useState({ lat: 18.490002, lng: 73.822441 }); // Your coordinates for location , 

  useEffect(() => {
    const firebaseConfig = {
      apiKey: "AIzaSyAjDqJBcwjFU5Td0azl7CaVBLkAV-hKOR4",
      authDomain: "saheli-app-9088f.firebaseapp.com",
      projectId: "saheli-app-9088f",
      storageBucket: "saheli-app-9088f.appspot.com",
      messagingSenderId: "635325370689",
      appId: "1:635325370689:web:2422bbf26dbbe774c3d1c0",
      measurementId: "G-C5QWS480VV"
    };

    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);

    const alertsRef = collection(db, "alerts");
    const q = query(alertsRef, orderBy("timestamp", "desc"), limit(1));

    const getLastDisplayedAlertId = () => localStorage.getItem("lastDisplayedAlertId");
    const setLastDisplayedAlertId = (id) => localStorage.setItem("lastDisplayedAlertId", id);

    const unsubscribeFirestore = onSnapshot(q, (snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === "added") {
          const alertData = change.doc.data();
          const alertId = change.doc.id;
          const lastDisplayedAlertId = getLastDisplayedAlertId();

          if (alertId !== lastDisplayedAlertId) {
            setLastDisplayedAlertId(alertId);
            triggerAlert(alertData.message);
          }
        }
      });
    });

    const ws = new WebSocket('ws://localhost:5000');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      triggerAlert(data.message);
    };

    const triggerAlert = (message) => {
      const buzzer = new Audio("/assets/buzzer.mp3");
      buzzer.play().catch(error => console.error("Error playing sound:", error));

      setAlertMessage(message);
      document.body.classList.add("alert-active");

      handleEmergencyCall(); // Automatically call emergency API when alert is triggered

      setTimeout(() => {
        document.body.classList.remove("alert-active");
        setAlertMessage("");
        buzzer.pause();
        buzzer.currentTime = 0;
      }, 10000);
    };

    // Function to handle the emergency call and send location
    const handleEmergencyCall = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5002/send-location", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            latitude: coordinates.lat,
            longitude: coordinates.lng,
            recipient_number: "+91 7775923217" // You can change or customize the recipient number
          })
        });

        const result = await response.json();
        if (response.ok) {
          console.log("Emergency call initiated and location sent successfully!");
        } else {
          console.error(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error(`Request failed: ${error.message}`);
      }
    };

    return () => {
      unsubscribeFirestore();
      ws.close();
    };
  }, []);

  return (
    <div className="app-container">
      <div className="alert-section">
        <h1>POLICE DASHBOARD</h1>
        <div className={`alert-message ${alertMessage ? 'active' : ''}`}>
          <h2>{alertMessage}</h2>
        </div>
      </div>
      <div className="map-section">
        <MapComponent coordinates={coordinates} />
      </div>
    </div>
  );
}

export default App;

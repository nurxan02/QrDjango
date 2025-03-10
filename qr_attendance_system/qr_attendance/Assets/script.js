"use strict";

function onScanSuccess(decodedText, decodedResult) {
  document.getElementById("result").innerText = "Oxunan QR: " + decodedText;
  sendToServer(decodedText);
  html5QrCode
    .stop()
    .then(() => {
      console.log("QR code scanning stopped.");
    })
    .catch((err) => {
      console.error("Failed to stop scanning:", err);
    });
}

let html5QrCode = new Html5Qrcode("reader");
html5QrCode.start(
  { facingMode: "environment" },
  { fps: 10, qrbox: 250 },
  onScanSuccess
);

function sendToServer(qrData) {
  let jsonData;
  try {
    jsonData = JSON.parse(qrData);
  } catch (error) {
    jsonData = { username: qrData };
  }

  fetch("http://127.0.0.1:8000/api/attendance/scan_qr/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
  })
    .then((response) => response.json())
    .then((data) => {
      let resultElement = document.getElementById("result");
      let resultTitle = document.getElementById("headTitle");
      if (data.message === "Checked-out" || data.message === "Checked-in") {
        resultElement.innerText = "Access granted";
        resultElement.style.color = "green";
        resultTitle.innerText = data.message;
        resultTitle.style.color = "green";
      } else if (data.message === "Today has already been logged in and out") {
        resultElement.innerText = "Access denied";
        resultElement.style.color = "red";
        resultTitle.innerText = data.message;
        resultTitle.style.color = "red";
      } else {
        resultElement.innerText = "Access denied";
        resultElement.style.color = "red";
        resultTitle.innerText = "You are not registered";
        resultTitle.style.color = "red";
        // alert("Cavab: " + data.message);
      }
      setTimeout(() => {
        location.reload();
      }, 3000);
    })
    .catch((error) => console.error("Error:", error));
}

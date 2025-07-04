# Tele Skincare System

A remote skincare support system for diagnosing skin conditions, guiding skincare methods, consulting dermatologists, and enabling medicine dispensing via smart pharmabox.

---

## 👥 Contributors

Special thanks to [Huy Trong Nguyen](https://github.com/nguyenhuytrong) and [Quoc Dat Bui](https://github.com/doquolo) for contributing dedicatedly to this project.

---

## 📦 Repository Structure

### 🖥️ **Module 1: Web App**

* **Skin condition diagnosis**: uses deep learning models trained on a custom dataset.
* **Chatbot**: uses ChatGPT API to support and answer patients' dermatology questions.
* **Map**: integrates Google Maps API to suggest nearby medical facilities.
* **Handbook**: guides patients in self-care.
* 🛠️ **Technology**:
    - *Frontend*: HTML, CSS, JavaScript
    - *Backend*: Python (Flask)
    - *Database*: MongoDB

---

### 🩹 **Module 2: Pharmabox**

* **Connect to server to fetch prescriptions**:
    - Flask (Python) server
    - Firebase database
    - Tablet for user interaction

* **Dispense medicine based on prescriptions**:
    - ESP32 microcontroller (UART communication)
    - Conveyor and actuators to move medicine to dispensing tray

* **Payment system**:
    - Payment API integration (Casso, PayOS, ...)

---


---

## 📞 Contact

For further questions or collaboration:
- 📧 huynghia05012007@gmail.com
- 👨‍💻 [LinkedIn link](https://www.linkedin.com/in/huy-nghia-nguyen-501010333/)
- 💼 [GitHub link](https://github.com/trongnghia2007)

---

> ✨ Feel free to star ⭐ this repository if you find it helpful!

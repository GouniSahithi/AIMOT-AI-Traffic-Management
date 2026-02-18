**🚦 AIMOT: AI-Powered Intelligent Monitoring and Optimization of Urban Traffic
📌 SIH 2024 | Problem ID: SIH1607
📖 Overview**
---

**AIMOT is an AI-based smart traffic management system designed to monitor real-time traffic flow and dynamically adjust signal timings to reduce congestion and prioritize emergency vehicles.**



**The system integrates:**

* **YOLOv8 for real-time vehicle detection**
* **MobileNetV2 for vehicle type classification**
* **Pygame for traffic simulation**
* **Streamlit for interactive dashboard visualization**
* 
**### 🚀 Features**

* **Real-time vehicle detection**
* **Vehicle type classification (car, bus, bike, ambulance, etc.)**
* **Lane-wise congestion calculation**
* **Dynamic traffic signal control**
* **Emergency vehicle prioritization**
* **Live dashboard analytics**
* 
**### 🛠 Tech Stack**

* **Python**
* **OpenCV**
* **YOLOv8 (Ultralytics)**
* **MobileNetV2**
* **Streamlit**
* **Pygame**
* 
**### 📂 Project Structure**

**├── dashboard.py**

**├── main\_pipeline.py**

**├── simulator/**

**├── signal\_controller/**

**├── mobilenet\_classifier/**

**├── yolo\_detection/**

**├── tools/**

**├── requirements.txt**



### **⚙️ Installation**

**git clone https://github.com/GouniSahithi/AIMOT-AI-Traffic-Management.git**

**cd AIMOT-AI-Traffic-Management**

**python -m venv venv**

**venv\\Scripts\\activate**

**pip install -r requirements.txt**



### **▶️ Run the Project**

**Run simulation:**



* **python simulator/traffic\_simulator.py**



**Run dashboard:**



* **python -m streamlit run dashboard.py**



### **🎯 Problem Addressed**



**Urban congestion due to static traffic signal systems.**



### **🌟 Future Enhancements**



* **Multi-intersection coordination**
* **Cloud deployment**
* **IoT sensor integration**
* **AI-based congestion prediction**

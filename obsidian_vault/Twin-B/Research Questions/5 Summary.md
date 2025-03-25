---
tags: 
source:
---
#summary #researchquestion 

# Objectives

1. To develop a model of the structure and energy consumption behavior in the Boonchupanitthan building for university executives to study energy-saving strategies.
2. To study methods for reducing electricity costs and saving energy at the university.
3. To create a tool that helps analyze and identify high-energy usage areas based on simulated scenarios derived from energy usage data extracted from historical data.
4. To assess the accuracy of the model through simulations using historical data.

# Optimization Research Question

**O1** : To develop a model of the structure and energy consumption behavior

- **RQ1** : Can Digital twin reduce the electricity consumption of the Boonchupanitthan building by what percentage, while maintaining a user comfort score of at least 80/100?

**O2** : To study methods for reducing electricity costs and saving energy

- **RQ2** : What percentage of energy load reduction can be achieved by an AI-based HVAC control system compared to manual settings in different climate zones?
- **RQ3** : By what percentage can Reinforcement Learning (DDPG vs. Q-Learning) reduce energy costs compared to Rule-Based Control?

**O3** : To create a tool that helps analyze and identify high-energy usage areas

- **RQ6** : How accurately can AI-Based Clustering (K-Means vs. DBSCAN) identify high energy usage areas compared to using historical averages?

**O4** : To assess the accuracy of the model through simulations using historical data

- **RQ4** : What is the predictive accuracy of Digital Twin's machine learning algorithm for energy consumption behavior using a validated statistical method?
- **RQ9** : How do digital twin models with a 5% accuracy loss compare to baseline models in terms of computational efficiency and reliability?


# Research Question
### **1. Energy Usage Behavior Simulation with Agent-Based Modeling**

- **Objective O1**: This method helps simulate and model the energy consumption behavior in the building, which is crucial for understanding how energy is being used.

- **RQ1:** How much can the use of a Digital Twin reduce electricity consumption in the Boonchupanitthan building while maintaining user comfort scores of at least 80/100?
- **RQ2:** How much can an AI-driven HVAC control system reduce energy consumption compared to manual settings in different climate zones?

**Research Method:**

- **Using MESA for Agent-Based Modeling (ABM):** Model the behavior of users in the building (students, faculty, staff) by simulating their movement and energy usage behavior based on real data such as Wi-Fi logs or CCTV footage.
- **Integration with EnergyPlus:** Use EnergyPlus to simulate energy usage within the building, such as HVAC and lighting systems, to assess energy consumption under various scenarios.
- **Evaluation:** Calculate energy savings and assess user comfort through simulation results.

### **2. Comparison of Energy Control Methods (AI-based HVAC vs. Manual Settings)**

- **Objective O2**: The purpose of this research method is to explore ways to reduce electricity costs and save energy. It focuses on comparing different control systems.

- **RQ2:** How much can an AI-driven HVAC control system reduce energy consumption compared to manual settings in different climate zones?
- **RQ3:** How much can Reinforcement Learning (DDPG vs. Q-Learning) reduce energy costs compared to Rule-Based control?

**Research Method:**

- **AI-based Control (Reinforcement Learning):** Use reinforcement learning techniques such as DDPG or Q-Learning to control the HVAC system in the building for different climate zones by simulating real-world usage.
- **Comparison with Manual Control:** Compare energy consumption results between AI-controlled systems and manually set controls.
- **Scenario Simulation:** Use MESA to simulate HVAC control in various scenarios to evaluate energy savings.

### **3. Energy Consumption Clustering (AI-Based Clustering)**

- **Objective O3**: This method is designed to identify high-energy usage areas, fulfilling the objective of creating a tool for analyzing and pinpointing energy inefficiencies.

- **RQ6:** How accurately can AI-Based Clustering (K-Means vs. DBSCAN) identify high-energy usage areas compared to historical average methods?

**Research Method:**

- **AI-based Clustering (K-Means vs. DBSCAN):** Use clustering techniques to analyze and identify areas with high energy consumption.
- **Comparison of Results:** Compare the accuracy of identifying high-energy areas between K-Means and DBSCAN against traditional methods, such as historical averages.

### **4. Model Accuracy Assessment**

- **Objective O4**: This method focuses on validating the accuracy of the energy consumption model using historical data, ensuring that the Digital Twin model performs reliably.

- **RQ4:** What is the prediction accuracy of the Digital Twin machine learning algorithm for energy consumption behavior using statistically validated methods?
- **RQ9:** How does a Digital Twin model with a 5% deviation compare to the baseline model in terms of computational performance and reliability?

**Research Method:**

- **Machine Learning and Statistical Methods:** Use machine learning algorithms to assess the accuracy of the Digital Twin model, employing validated statistical techniques (e.g., Cross-Validation, MAPE, RMSE) to evaluate accuracy.
- **Model Comparison:** Compare the performance of the Digital Twin model with a 5% deviation against the baseline model, using performance and reliability metrics derived from simulations.

### **5. Use of HPC to Enhance Computational Efficiency**

- **Objective O4**: This method is crucial for enhancing computational efficiency when processing complex energy models, addressing the need for faster and more reliable simulations.

- **RQ9:** How does a Digital Twin model with a 5% deviation compare to the baseline model in terms of computational performance and reliability?

**Research Method:**

- **Using HPC (LANTA):** Use HPC tools for processing complex models such as Twin-B, simulating different scenarios to reduce energy consumption and adjust project variables.
- **Evaluation of Computational Results:** Compare computational performance between using HPC and non-HPC methods for processing.

# Thai
### **วัตถุประสงค์ของการวิจัย**

1. เพื่อพัฒนาแบบจำลองพฤติกรรมการใช้พลังงานในอาคารบุญชูปณิธาน มหาวิทยาลัยธรรมศาสตร์ ศูนย์ลำปาง
    
2. เพื่อศึกษาแนวทางในลดค่าไฟฟ้าและประหยัดพลังงานพลังงานในมหาวิทยาลัย
    
3. เพื่อสร้างเครื่องมือที่ช่วยวิเคราะห์และระบุพื้นที่ที่มีการใช้พลังงานสูง จากการจำลองสถานการณ์สมมุติตามรูปการใช้พลังงานที่สกัดได้จากข้อมูลย้อนหลัง
    
4. เพื่อประเมินความถูกต้องของแบบจำลอง ผ่านการจำลองสถานการณ์โดยใช้ข้อมูลในอดีต

---

### **คำถามการวิจัยด้านการเพิ่มประสิทธิภาพ (Optimization Research Question)**

**O1**: เพื่อพัฒนาแบบจำลองพฤติกรรมการใช้พลังงานในอาคารบุญชูปณิธาน มหาวิทยาลัยธรรมศาสตร์ ศูนย์ลำปาง

- **RQ1**: Digital Twin สามารถลดการใช้พลังงานไฟฟ้าในอาคารบุญชุปนิษฐานได้กี่เปอร์เซ็นต์ โดยยังคงระดับความสะดวกสบายของผู้ใช้ไม่น้อยกว่า 80/100?
    

**O2**: เพื่อศึกษาแนวทางในลดค่าไฟฟ้าและประหยัดพลังงานพลังงานในมหาวิทยาลัย

- **RQ2**: ระบบควบคุม HVAC อัตโนมัติที่ใช้ AI สามารถลดภาระโหลดพลังงานได้กี่เปอร์เซ็นต์เมื่อเทียบกับการตั้งค่าด้วยมือในเขตภูมิอากาศที่แตกต่างกัน?
    
- **RQ3**: Reinforcement Learning (DDPG vs. Q-Learning) สามารถลดต้นทุนพลังงานได้กี่เปอร์เซ็นต์เมื่อเทียบกับ Rule-Based Control?
    

**O3**: เพื่อสร้างเครื่องมือที่ช่วยวิเคราะห์และระบุพื้นที่ที่มีการใช้พลังงานสูง จากการจำลองสถานการณ์สมมุติตามรูปการใช้พลังงานที่สกัดได้จากข้อมูลย้อนหลัง

- **RQ6**: AI-Based Clustering (K-Means vs. DBSCAN) สามารถระบุพื้นที่ใช้พลังงานสูงได้แม่นยำเพียงใดเมื่อเทียบกับวิธีการเฉลี่ยจากข้อมูลในอดีต?
    

**O4**: เพื่อประเมินความถูกต้องของแบบจำลอง ผ่านการจำลองสถานการณ์โดยใช้ข้อมูลในอดีต

- **RQ4**: อัลกอริธึม Machine Learning ของ Digital Twin มีความแม่นยำในการพยากรณ์พฤติกรรมการใช้พลังงานเพียงใดโดยใช้วิธีการทางสถิติที่ผ่านการตรวจสอบ?
    
- **RQ9**: โมเดล Digital Twin ที่มีค่าความคลาดเคลื่อน 5% เปรียบเทียบกับโมเดลพื้นฐานในแง่ของประสิทธิภาพการคำนวณและความน่าเชื่อถืออย่างไร?
    

---

### **คำถามการวิจัยหลัก**

#### **1. การจำลองพฤติกรรมการใช้พลังงานด้วย Agent-Based Modeling**

- **O1**: เพื่อพัฒนาแบบจำลองพฤติกรรมการใช้พลังงานในอาคารบุญชูปณิธาน มหาวิทยาลัยธรรมศาสตร์ ศูนย์ลำปาง
    
- **RQ1**: Digital Twin สามารถลดการใช้พลังงานไฟฟ้าได้มากน้อยเพียงใดในขณะที่รักษาค่าความสะดวกสบายของผู้ใช้ไม่น้อยกว่า 80/100?
    
- **RQ2**: ระบบควบคุม HVAC ที่ใช้ AI สามารถลดการใช้พลังงานได้มากเพียงใดเมื่อเทียบกับการตั้งค่าด้วยมือในเขตภูมิอากาศต่างๆ?
    

**วิธีการวิจัย:**

- **ใช้ MESA สำหรับ Agent-Based Modeling (ABM):** จำลองพฤติกรรมผู้ใช้ภายในอาคาร (นักศึกษา อาจารย์ บุคลากร) โดยใช้ข้อมูลจริง เช่น บันทึก Wi-Fi หรือกล้องวงจรปิด
    
- **เชื่อมโยงกับ EnergyPlus:** จำลองการใช้พลังงานภายในอาคาร เช่น ระบบ HVAC และไฟฟ้า เพื่อวิเคราะห์การใช้พลังงานภายใต้สถานการณ์ที่แตกต่างกัน
    
- **การประเมินผล:** คำนวณการประหยัดพลังงานและวิเคราะห์ระดับความสะดวกสบายของผู้ใช้งาน
    

---

#### **2. การเปรียบเทียบวิธีการควบคุมพลังงาน (AI-based HVAC vs. Manual Settings)**

- **O2**: เพื่อศึกษาแนวทางในลดค่าไฟฟ้าและประหยัดพลังงานพลังงานในมหาวิทยาลัย
    
- **RQ2**: ระบบ HVAC ที่ควบคุมด้วย AI สามารถลดการใช้พลังงานได้มากเพียงใดเมื่อเทียบกับการตั้งค่าด้วยมือในเขตภูมิอากาศที่แตกต่างกัน?
    
- **RQ3**: Reinforcement Learning (DDPG vs. Q-Learning) สามารถลดต้นทุนพลังงานได้กี่เปอร์เซ็นต์เมื่อเทียบกับ Rule-Based Control?
    

**วิธีการวิจัย:**

- **ควบคุม HVAC ด้วย AI (Reinforcement Learning):** ใช้เทคนิค DDPG และ Q-Learning ในการควบคุม HVAC โดยจำลองการใช้งานจริง
    
- **เปรียบเทียบกับการควบคุมแบบ Manual:** วิเคราะห์ปริมาณการใช้พลังงานระหว่างระบบอัตโนมัติและการตั้งค่าด้วยมือ
    
- **การจำลองสถานการณ์:** ใช้ MESA เพื่อจำลองการควบคุม HVAC ในเงื่อนไขที่แตกต่างกันเพื่อลดการใช้พลังงาน
    

---

#### **3. การจัดกลุ่มการใช้พลังงานด้วย AI-Based Clustering**

- **O3**: เพื่อสร้างเครื่องมือที่ช่วยวิเคราะห์และระบุพื้นที่ที่มีการใช้พลังงานสูง จากการจำลองสถานการณ์สมมุติตามรูปการใช้พลังงานที่สกัดได้จากข้อมูลย้อนหลัง
    
- **RQ6**: AI-Based Clustering (K-Means vs. DBSCAN) สามารถระบุพื้นที่ใช้พลังงานสูงได้แม่นยำเพียงใดเมื่อเทียบกับวิธีการเฉลี่ยจากข้อมูลในอดีต?
    

**วิธีการวิจัย:**

- **AI-Based Clustering (K-Means vs. DBSCAN):** ใช้เทคนิคการจัดกลุ่มเพื่อวิเคราะห์และระบุพื้นที่ที่ใช้พลังงานสูง
    
- **เปรียบเทียบผลลัพธ์:** วิเคราะห์ความแม่นยำของการระบุพื้นที่ใช้พลังงานสูงระหว่าง K-Means, DBSCAN และวิธีเฉลี่ยจากข้อมูลในอดีต
    

---

#### **4. การประเมินความแม่นยำของโมเดล**

- **O4**: เพื่อประเมินความถูกต้องของแบบจำลอง ผ่านการจำลองสถานการณ์โดยใช้ข้อมูลในอดีต
    
- **RQ4**: อัลกอริธึม Machine Learning ของ Digital Twin มีความแม่นยำในการพยากรณ์พฤติกรรมการใช้พลังงานเพียงใดโดยใช้วิธีการทางสถิติที่ผ่านการตรวจสอบ?
    
- **RQ9**: โมเดล Digital Twin ที่มีค่าความคลาดเคลื่อน 5% เปรียบเทียบกับโมเดลพื้นฐานในแง่ของประสิทธิภาพการคำนวณและความน่าเชื่อถืออย่างไร?
    

**วิธีการวิจัย:**

- **Machine Learning และวิธีสถิติ:** ใช้เทคนิคทางสถิติ เช่น Cross-Validation, MAPE และ RMSE เพื่อประเมินความแม่นยำของโมเดล Digital Twin
    
- **เปรียบเทียบโมเดล:** วิเคราะห์ประสิทธิภาพของ Digital Twin ที่มีค่าความคลาดเคลื่อน 5% กับโมเดลพื้นฐาน
    

---

#### **5. การใช้ HPC เพื่อเพิ่มประสิทธิภาพการคำนวณ**

- **O4**: ปรับปรุงประสิทธิภาพการคำนวณของการจำลองโมเดลพลังงาน เพื่อให้ได้ผลลัพธ์ที่รวดเร็วและแม่นยำมากขึ้น
    
- **RQ9**: โมเดล Digital Twin ที่มีค่าความคลาดเคลื่อน 5% เปรียบเทียบกับโมเดลพื้นฐานในแง่ของประสิทธิภาพการคำนวณและความน่าเชื่อถืออย่างไร?
    

**วิธีการวิจัย:**

- **ใช้ HPC (LANTA):** ใช้ HPC เพื่อจำลอง Twin-B และประเมินตัวแปรโครงการต่างๆ
    
- **เปรียบเทียบผลการคำนวณ:** วิเคราะห์ความเร็วและความถูกต้องของการจำลองระหว่างวิธีที่ใช้ HPC และวิธีที่ไม่ใช้ HPC
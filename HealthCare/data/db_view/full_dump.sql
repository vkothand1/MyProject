PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE patients (
  patient_id TEXT PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  birth_year INTEGER NOT NULL,
  sex_at_birth TEXT CHECK (sex_at_birth IN ('F','M','X')) NOT NULL,
  preferred_language TEXT NOT NULL,
  health_literacy_level TEXT CHECK (health_literacy_level IN ('basic','intermediate')) NOT NULL,
  timezone TEXT NOT NULL,
  created_at TEXT NOT NULL
);
INSERT INTO patients VALUES('P001','Ava','Patel',1989,'F','en','intermediate','America/New_York','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P002','Noah','Johnson',1978,'M','en','basic','America/Chicago','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P003','Mia','Garcia',1994,'F','es','basic','America/Los_Angeles','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P004','Ethan','Kim',1967,'M','en','intermediate','America/New_York','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P005','Sophia','Nguyen',1983,'F','en','intermediate','America/Denver','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P006','Liam','Brown',1959,'M','en','basic','America/Chicago','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P007','Isabella','Martinez',2000,'F','es','intermediate','America/Los_Angeles','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P008','Oliver','Davis',1971,'M','en','intermediate','America/New_York','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P009','Charlotte','Wilson',1991,'F','en','basic','America/Chicago','2026-01-29T19:42:27Z');
INSERT INTO patients VALUES('P010','James','Anderson',1986,'M','en','intermediate','America/Seattle','2026-01-29T19:42:27Z');
CREATE TABLE encounters (
  encounter_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL,
  encounter_date TEXT NOT NULL,
  encounter_type TEXT NOT NULL,
  reason_for_visit TEXT NOT NULL,
  diagnosis_summary TEXT NOT NULL,
  provider_specialty TEXT NOT NULL,
  followup_instructions TEXT NOT NULL,
  care_team_contact TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
INSERT INTO encounters VALUES('E_56b16cd2d1','P001','2025-10-14','specialist','Heartburn and reflux follow-up','GERD; lifestyle counseling','Gastroenterology','Avoid late meals, elevate head of bed, limit trigger foods. Contact clinic for trouble swallowing, black stools, or unintentional weight loss.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_b280a125e8','P001','2025-11-13','primary_care','Review cholesterol results and cardiovascular risk','Hyperlipidemia; lifestyle counseling','Cardiology','Heart-healthy diet emphasized. Repeat lipid panel in 3-6 months. Discuss medication options if LDL remains elevated.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_bda378c238','P001','2025-12-13','urgent_care','Follow-up for blood pressure and medication refill','Hypertension; reviewed home BP log','Primary Care','Continue home BP checks 3-4x/week. Follow up in 3 months. Seek urgent care for severe headache, chest pain, or shortness of breath.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_5aa2fc568c','P002','2025-11-25','urgent_care','Follow-up for blood pressure and medication refill','Hypertension; reviewed home BP log','Primary Care','Continue home BP checks 3-4x/week. Follow up in 3 months. Seek urgent care for severe headache, chest pain, or shortness of breath.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_e2023f0d15','P002','2025-12-25','primary_care','Diabetes check-in and lab review','Type 2 diabetes; A1c monitoring','Endocrinology','Continue lifestyle changes. Repeat A1c in 3 months. Contact clinic if recurrent low blood sugar symptoms or vomiting/dehydration.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_9bbb18e79c','P002','2026-01-24','specialist','Follow-up for blood pressure and medication refill','Hypertension; reviewed home BP log','Primary Care','Continue home BP checks 3-4x/week. Follow up in 3 months. Seek urgent care for severe headache, chest pain, or shortness of breath.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_903769d23d','P002','2026-02-23','urgent_care','Review cholesterol results and cardiovascular risk','Hyperlipidemia; lifestyle counseling','Cardiology','Heart-healthy diet emphasized. Repeat lipid panel in 3-6 months. Discuss medication options if LDL remains elevated.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_54bb098594','P003','2025-03-13','telehealth','Asthma symptom review and inhaler technique','Asthma; reviewed triggers and rescue inhaler use','Pulmonology','Continue controller/rescue plan as prescribed. Seek urgent care for worsening wheeze, trouble speaking in full sentences, or blue lips.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_b834dfb8a7','P004','2025-06-23','primary_care','Asthma symptom review and inhaler technique','Asthma; reviewed triggers and rescue inhaler use','Pulmonology','Continue controller/rescue plan as prescribed. Seek urgent care for worsening wheeze, trouble speaking in full sentences, or blue lips.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_c531dcb3ad','P004','2025-07-23','primary_care','Asthma symptom review and inhaler technique','Asthma; reviewed triggers and rescue inhaler use','Pulmonology','Continue controller/rescue plan as prescribed. Seek urgent care for worsening wheeze, trouble speaking in full sentences, or blue lips.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_59fa99c509','P005','2025-07-23','specialist','Asthma symptom review and inhaler technique','Asthma; reviewed triggers and rescue inhaler use','Pulmonology','Continue controller/rescue plan as prescribed. Seek urgent care for worsening wheeze, trouble speaking in full sentences, or blue lips.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_7ea17354ce','P005','2025-08-22','urgent_care','Cough and sore throat for 4 days','Upper respiratory infection symptoms; supportive care discussed','Urgent Care','Supportive care: fluids, rest. Return if fever persists >3 days, worsening shortness of breath, or chest pain.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_0b735b3d73','P005','2025-09-21','urgent_care','Follow-up for blood pressure and medication refill','Hypertension; reviewed home BP log','Primary Care','Continue home BP checks 3-4x/week. Follow up in 3 months. Seek urgent care for severe headache, chest pain, or shortness of breath.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_e0b8658ce0','P005','2025-10-21','telehealth','Heartburn and reflux follow-up','GERD; lifestyle counseling','Gastroenterology','Avoid late meals, elevate head of bed, limit trigger foods. Contact clinic for trouble swallowing, black stools, or unintentional weight loss.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_d3b0b61ecf','P006','2025-10-31','specialist','Diabetes check-in and lab review','Type 2 diabetes; A1c monitoring','Endocrinology','Continue lifestyle changes. Repeat A1c in 3 months. Contact clinic if recurrent low blood sugar symptoms or vomiting/dehydration.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_b2ce31819a','P007','2025-12-10','primary_care','Cough and sore throat for 4 days','Upper respiratory infection symptoms; supportive care discussed','Urgent Care','Supportive care: fluids, rest. Return if fever persists >3 days, worsening shortness of breath, or chest pain.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_23f7fe6b08','P007','2026-01-09','telehealth','Asthma symptom review and inhaler technique','Asthma; reviewed triggers and rescue inhaler use','Pulmonology','Continue controller/rescue plan as prescribed. Seek urgent care for worsening wheeze, trouble speaking in full sentences, or blue lips.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_58267622eb','P007','2026-02-08','primary_care','Cough and sore throat for 4 days','Upper respiratory infection symptoms; supportive care discussed','Urgent Care','Supportive care: fluids, rest. Return if fever persists >3 days, worsening shortness of breath, or chest pain.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_7993abca2d','P007','2026-03-10','specialist','Heartburn and reflux follow-up','GERD; lifestyle counseling','Gastroenterology','Avoid late meals, elevate head of bed, limit trigger foods. Contact clinic for trouble swallowing, black stools, or unintentional weight loss.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_aeb2b2529d','P008','2025-03-10','specialist','Review cholesterol results and cardiovascular risk','Hyperlipidemia; lifestyle counseling','Cardiology','Heart-healthy diet emphasized. Repeat lipid panel in 3-6 months. Discuss medication options if LDL remains elevated.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_e51844a6ee','P008','2025-04-09','primary_care','Thyroid medication follow-up','Hypothyroidism; monitoring TSH','Endocrinology','Take levothyroxine on an empty stomach, avoid taking with calcium/iron. Recheck TSH in 6-8 weeks after any dose change.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_61eab10dd4','P008','2025-05-09','primary_care','Thyroid medication follow-up','Hypothyroidism; monitoring TSH','Endocrinology','Take levothyroxine on an empty stomach, avoid taking with calcium/iron. Recheck TSH in 6-8 weeks after any dose change.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_8947b1056a','P009','2025-10-25','urgent_care','Thyroid medication follow-up','Hypothyroidism; monitoring TSH','Endocrinology','Take levothyroxine on an empty stomach, avoid taking with calcium/iron. Recheck TSH in 6-8 weeks after any dose change.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_b74cb823bf','P009','2025-11-24','urgent_care','Thyroid medication follow-up','Hypothyroidism; monitoring TSH','Endocrinology','Take levothyroxine on an empty stomach, avoid taking with calcium/iron. Recheck TSH in 6-8 weeks after any dose change.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_92f770b8df','P009','2025-12-24','urgent_care','Cough and sore throat for 4 days','Upper respiratory infection symptoms; supportive care discussed','Urgent Care','Supportive care: fluids, rest. Return if fever persists >3 days, worsening shortness of breath, or chest pain.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_fb56a0bc95','P010','2025-06-30','specialist','Diabetes check-in and lab review','Type 2 diabetes; A1c monitoring','Endocrinology','Continue lifestyle changes. Repeat A1c in 3 months. Contact clinic if recurrent low blood sugar symptoms or vomiting/dehydration.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_52ef345d67','P010','2025-07-30','urgent_care','Diabetes check-in and lab review','Type 2 diabetes; A1c monitoring','Endocrinology','Continue lifestyle changes. Repeat A1c in 3 months. Contact clinic if recurrent low blood sugar symptoms or vomiting/dehydration.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_a2c746f8b1','P010','2025-08-29','urgent_care','Follow-up for blood pressure and medication refill','Hypertension; reviewed home BP log','Primary Care','Continue home BP checks 3-4x/week. Follow up in 3 months. Seek urgent care for severe headache, chest pain, or shortness of breath.','Call clinic at (555) 010-2000');
INSERT INTO encounters VALUES('E_8a3eb4bf3f','P010','2025-09-28','telehealth','Review cholesterol results and cardiovascular risk','Hyperlipidemia; lifestyle counseling','Cardiology','Heart-healthy diet emphasized. Repeat lipid panel in 3-6 months. Discuss medication options if LDL remains elevated.','Call clinic at (555) 010-2000');
CREATE TABLE clinical_notes (
  note_id TEXT PRIMARY KEY,
  encounter_id TEXT NOT NULL,
  patient_id TEXT NOT NULL,
  note_type TEXT NOT NULL,
  note_text TEXT NOT NULL,
  created_at TEXT NOT NULL,
  author_role TEXT NOT NULL,
  FOREIGN KEY(encounter_id) REFERENCES encounters(encounter_id),
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
INSERT INTO clinical_notes VALUES('N_475226e99a','E_56b16cd2d1','P001','visit_note',replace('Subjective: Follow-up for reflux symptoms. Improved with PPI and diet changes.\nAssessment/Plan: Reviewed lifestyle measures and appropriate use of acid suppression therapy. Discussed alarm symptoms that require prompt evaluation.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_f1d1e13873','E_b280a125e8','P001','visit_note',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_e2770a905a','E_bda378c238','P001','visit_note',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_59f2496574','E_5aa2fc568c','P002','visit_note',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_08ead324c0','E_5aa2fc568c','P002','discharge_summary',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_8cc97ac0b2','E_e2023f0d15','P002','visit_note',replace('Subjective: Follow-up for type 2 diabetes. No episodes of severe hypoglycemia reported. Discussed diet, activity, and monitoring.\nAssessment/Plan: Reviewed A1c goals and importance of consistency. Ordered A1c and CMP. Provided education on signs of low blood sugar and when to seek care.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_d7b30de35c','E_9bbb18e79c','P002','visit_note',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_0e2d1182f1','E_903769d23d','P002','visit_note',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_f5f5b34c84','E_903769d23d','P002','discharge_summary',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_54f2bb7820','E_54bb098594','P003','visit_note',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_15c516fd8c','E_b834dfb8a7','P004','visit_note',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_ecef946c8b','E_c531dcb3ad','P004','visit_note',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_dfeb559f56','E_59fa99c509','P005','visit_note',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_aadf1dd377','E_59fa99c509','P005','discharge_summary',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_3bfc56dca7','E_7ea17354ce','P005','visit_note',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_f965cea28f','E_0b735b3d73','P005','visit_note',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_eb94db34e5','E_0b735b3d73','P005','discharge_summary',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_2b9b113bb9','E_e0b8658ce0','P005','visit_note',replace('Subjective: Follow-up for reflux symptoms. Improved with PPI and diet changes.\nAssessment/Plan: Reviewed lifestyle measures and appropriate use of acid suppression therapy. Discussed alarm symptoms that require prompt evaluation.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_30e28a9a21','E_e0b8658ce0','P005','discharge_summary',replace('Subjective: Follow-up for reflux symptoms. Improved with PPI and diet changes.\nAssessment/Plan: Reviewed lifestyle measures and appropriate use of acid suppression therapy. Discussed alarm symptoms that require prompt evaluation.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_db92db5415','E_d3b0b61ecf','P006','visit_note',replace('Subjective: Follow-up for type 2 diabetes. No episodes of severe hypoglycemia reported. Discussed diet, activity, and monitoring.\nAssessment/Plan: Reviewed A1c goals and importance of consistency. Ordered A1c and CMP. Provided education on signs of low blood sugar and when to seek care.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_ec6a18876b','E_d3b0b61ecf','P006','discharge_summary',replace('Subjective: Follow-up for type 2 diabetes. No episodes of severe hypoglycemia reported. Discussed diet, activity, and monitoring.\nAssessment/Plan: Reviewed A1c goals and importance of consistency. Ordered A1c and CMP. Provided education on signs of low blood sugar and when to seek care.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_b5b446dc33','E_b2ce31819a','P007','visit_note',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_11bea4bfe0','E_b2ce31819a','P007','discharge_summary',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_44a022ad27','E_23f7fe6b08','P007','visit_note',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_daf3f81e8f','E_23f7fe6b08','P007','discharge_summary',replace('Subjective: Follow-up for asthma. Uses rescue inhaler a few times per week. No recent hospitalizations.\nAssessment/Plan: Reviewed inhaler technique, trigger avoidance, and action plan. Discussed when to seek urgent evaluation for worsening symptoms.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_ecfd53b71d','E_58267622eb','P007','visit_note',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_6949e59bdd','E_7993abca2d','P007','visit_note',replace('Subjective: Follow-up for reflux symptoms. Improved with PPI and diet changes.\nAssessment/Plan: Reviewed lifestyle measures and appropriate use of acid suppression therapy. Discussed alarm symptoms that require prompt evaluation.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_f6242218a8','E_aeb2b2529d','P008','visit_note',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_49025aa923','E_aeb2b2529d','P008','discharge_summary',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_4f1c68f87f','E_e51844a6ee','P008','visit_note',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_9380347579','E_e51844a6ee','P008','discharge_summary',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_a94d6448d2','E_61eab10dd4','P008','visit_note',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_635bcb888e','E_8947b1056a','P009','visit_note',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_1c56e4ecd6','E_8947b1056a','P009','discharge_summary',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_54594a6f7f','E_b74cb823bf','P009','visit_note',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_040c5544ee','E_b74cb823bf','P009','discharge_summary',replace('Subjective: Follow-up for hypothyroidism. Reports fatigue improved. Denies palpitations.\nAssessment/Plan: Reviewed proper timing of levothyroxine and interactions (calcium/iron). Ordered TSH and free T4 for monitoring.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_f8a5599bba','E_92f770b8df','P009','visit_note',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_589080b43a','E_92f770b8df','P009','discharge_summary',replace('Subjective: Presents with cough, congestion, sore throat x4 days. No shortness of breath at rest.\nAssessment/Plan: Discussed supportive care and warning signs. Considered testing as appropriate. Advised follow-up if symptoms worsen or persist.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','nurse_practitioner');
INSERT INTO clinical_notes VALUES('N_d19e9fa7c4','E_fb56a0bc95','P010','visit_note',replace('Subjective: Follow-up for type 2 diabetes. No episodes of severe hypoglycemia reported. Discussed diet, activity, and monitoring.\nAssessment/Plan: Reviewed A1c goals and importance of consistency. Ordered A1c and CMP. Provided education on signs of low blood sugar and when to seek care.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_2b90e366b2','E_52ef345d67','P010','visit_note',replace('Subjective: Follow-up for type 2 diabetes. No episodes of severe hypoglycemia reported. Discussed diet, activity, and monitoring.\nAssessment/Plan: Reviewed A1c goals and importance of consistency. Ordered A1c and CMP. Provided education on signs of low blood sugar and when to seek care.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_3a8974c2b7','E_a2c746f8b1','P010','visit_note',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.','\n',char(10)),'2026-01-29T19:42:27Z','nurse');
INSERT INTO clinical_notes VALUES('N_ecd37bc144','E_a2c746f8b1','P010','discharge_summary',replace('Subjective: Patient here for BP follow-up. Reports occasional headaches but no chest pain, no shortness of breath. Taking antihypertensive as prescribed.\nAssessment/Plan: Hypertension discussed. Reinforced low-sodium diet, exercise, and medication adherence. Ordered basic metabolic panel to monitor kidney function and electrolytes.\nReturn precautions: Go to ER for chest pain, fainting, severe shortness of breath, or neurologic symptoms.\nDischarge: Follow the instructions above. Use patient portal messaging for non-urgent questions.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
INSERT INTO clinical_notes VALUES('N_6afd7d92ec','E_8a3eb4bf3f','P010','visit_note',replace('Subjective: Here to review lipid panel and discuss cardiovascular risk factors. No chest pain on exertion.\nAssessment/Plan: Discussed LDL/HDL/triglycerides and general lifestyle strategies. Reviewed medication adherence if on statin. Ordered repeat lipid panel.','\n',char(10)),'2026-01-29T19:42:27Z','physician');
CREATE TABLE labs (
  lab_result_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL,
  ordered_date TEXT NOT NULL,
  result_date TEXT NOT NULL,
  loinc_code TEXT,
  test_name TEXT NOT NULL,
  value_numeric REAL,
  value_text TEXT,
  unit TEXT,
  ref_range_low REAL,
  ref_range_high REAL,
  flag TEXT CHECK (flag IN ('low','high','normal','abnormal')) NOT NULL,
  lab_source TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
INSERT INTO labs VALUES('L_9fa12ec449','P001','2025-06-09','2025-06-09','4548-4','Hemoglobin A1c',4.94000000000000039,NULL,'%',4.0,5.599999999999999645,'normal','Quest');
INSERT INTO labs VALUES('L_42dab00304','P002','2025-11-06','2025-11-06','1558-6','Glucose, fasting',84.85999999999999944,NULL,'mg/dL',70.0,99.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_6c3bdb9d9e','P003','2025-02-08','2025-02-08','2345-7','Glucose, random',80.01999999999999603,NULL,'mg/dL',70.0,140.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_fdfd4f2a7f','P004','2025-03-29','2025-03-29','2160-0','Creatinine',0.8900000000000000133,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a08b1baede','P005','2025-05-08','2025-05-08','33914-3','eGFR',93.0,NULL,'mL/min/1.73m2',60.0,120.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_b7bbd58883','P006','2025-10-04','2025-10-04','3094-0','BUN',21.60000000000000143,NULL,'mg/dL',7.0,20.0,'high','LabCorp');
INSERT INTO labs VALUES('L_fc3e9625b3','P007','2025-12-14','2025-12-14','2951-2','Sodium',147.9099999999999966,NULL,'mmol/L',135.0,145.0,'high','LabCorp');
INSERT INTO labs VALUES('L_5c4e87803b','P008','2025-12-27','2025-12-27','2823-3','Potassium',5.450000000000000177,NULL,'mmol/L',3.5,5.099999999999999645,'high','Quest');
INSERT INTO labs VALUES('L_c2e60fe3aa','P009','2025-03-07','2025-03-07','2075-0','Chloride',99.7800000000000011,NULL,'mmol/L',98.0,107.0,'normal','Quest');
INSERT INTO labs VALUES('L_e9eab112d7','P010','2025-05-16','2025-05-16','2028-9','CO2 (Bicarbonate)',24.44999999999999929,NULL,'mmol/L',22.0,29.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_e5d0707e08','P001','2025-11-18','2025-11-18','17861-6','Calcium',9.71000000000000086,NULL,'mg/dL',8.599999999999999645,10.19999999999999928,'normal','Quest');
INSERT INTO labs VALUES('L_a8d98e4432','P002','2025-10-19','2025-10-19','1742-6','ALT',19.94000000000000127,NULL,'U/L',7.0,56.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_28d030d533','P003','2025-07-08','2025-07-08','1920-8','AST',41.86999999999999745,NULL,'U/L',10.0,40.0,'high','LabCorp');
INSERT INTO labs VALUES('L_264974f558','P004','2025-11-24','2025-11-24','6768-6','Alkaline phosphatase',75.81999999999999317,NULL,'U/L',44.0,147.0,'normal','Quest');
INSERT INTO labs VALUES('L_35e39aea6a','P005','2025-10-16','2025-10-16','1975-2','Total bilirubin',0.4099999999999999756,NULL,'mg/dL',0.1000000000000000055,1.199999999999999956,'normal','LabCorp');
INSERT INTO labs VALUES('L_44caa57695','P006','2025-04-27','2025-04-27','1751-7','Albumin',3.919999999999999929,NULL,'g/dL',3.5,5.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_af61b1f866','P007','2025-09-09','2025-09-09','2093-3','Total cholesterol',138.3799999999999955,NULL,'mg/dL',0.0,200.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_e6d6f89cbe','P008','2025-09-29','2025-09-29','13457-7','LDL cholesterol (calculated)',38.45000000000000285,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a6b9f6b6d7','P009','2025-12-26','2025-12-26','2085-9','HDL cholesterol',65.59999999999999431,NULL,'mg/dL',40.0,999.0,'normal','Quest');
INSERT INTO labs VALUES('L_b1da347156','P010','2025-08-30','2025-08-30','2571-8','Triglycerides',180.740000000000009,NULL,'mg/dL',0.0,150.0,'high','Quest');
INSERT INTO labs VALUES('L_39e6ee1a12','P001','2025-11-29','2025-11-29','3016-3','TSH',-1.030000000000000026,NULL,'uIU/mL',0.4000000000000000222,4.0,'low','Quest');
INSERT INTO labs VALUES('L_0d5cd9109d','P002','2025-02-24','2025-02-24','3024-7','Free T4',1.389999999999999903,NULL,'ng/dL',0.8000000000000000444,1.800000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_14d5be4885','P003','2025-05-09','2025-05-09','718-7','Hemoglobin',13.5,NULL,'g/dL',12.0,16.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_d0ac542dbe','P004','2025-11-27','2025-11-27','6690-2','WBC',5.370000000000000106,NULL,'10^3/uL',4.0,11.0,'normal','Quest');
INSERT INTO labs VALUES('L_e9ba1a1b13','P005','2025-09-29','2025-09-29','777-3','Platelets',222.8499999999999944,NULL,'10^3/uL',150.0,450.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_ea070bf381','P006','2025-07-23','2025-07-23','2276-4','Ferritin',200.5999999999999944,NULL,'ng/mL',15.0,150.0,'high','Quest');
INSERT INTO labs VALUES('L_b0ba09498b','P007','2025-11-27','2025-11-27','35365-6','Vitamin D (25-OH)',27.0799999999999983,NULL,'ng/mL',20.0,50.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_134a47762d','P008','2025-12-26','2025-12-26','1988-5','CRP',-0.930000000000000048,NULL,'mg/L',0.0,10.0,'low','LabCorp');
INSERT INTO labs VALUES('L_d6186f3cc6','P009','2025-03-10','2025-03-10','2888-6','Urinalysis - Protein',NULL,'trace','negative/trace',NULL,NULL,'normal','LabCorp');
INSERT INTO labs VALUES('L_964e989ebc','P010','2025-07-14','2025-07-14','2349-9','Urinalysis - Glucose',NULL,'negative','negative',NULL,NULL,'normal','LabCorp');
INSERT INTO labs VALUES('L_e2dad2dda9','P001','2025-02-21','2025-02-21','4548-4','Hemoglobin A1c',3.740000000000000213,NULL,'%',4.0,5.599999999999999645,'low','In-house Lab');
INSERT INTO labs VALUES('L_698c993cc5','P001','2025-08-23','2025-08-23','13457-7','LDL cholesterol (calculated)',71.09000000000000341,NULL,'mg/dL',0.0,100.0,'normal','Quest');
INSERT INTO labs VALUES('L_71d272447f','P001','2025-11-13','2025-11-13','3016-3','TSH',5.629999999999999894,NULL,'uIU/mL',0.4000000000000000222,4.0,'high','LabCorp');
INSERT INTO labs VALUES('L_dbacdbc353','P001','2025-04-26','2025-04-26','13457-7','LDL cholesterol (calculated)',79.81999999999999317,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a9af9a4526','P001','2025-11-04','2025-11-04','777-3','Platelets',63.9200000000000017,NULL,'10^3/uL',150.0,450.0,'low','Quest');
INSERT INTO labs VALUES('L_fe5ef3a935','P001','2025-04-10','2025-04-10','2093-3','Total cholesterol',144.240000000000009,NULL,'mg/dL',0.0,200.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_004981a4c3','P001','2025-08-31','2025-08-31','13457-7','LDL cholesterol (calculated)',-45.60000000000000142,NULL,'mg/dL',0.0,100.0,'low','In-house Lab');
INSERT INTO labs VALUES('L_c608c26a4d','P001','2025-05-06','2025-05-06','1558-6','Glucose, fasting',77.53000000000000113,NULL,'mg/dL',70.0,99.0,'normal','Quest');
INSERT INTO labs VALUES('L_5988aecb46','P001','2025-05-20','2025-05-20','13457-7','LDL cholesterol (calculated)',29.80999999999999873,NULL,'mg/dL',0.0,100.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_ad53de5ed9','P001','2025-09-09','2025-09-09','2349-9','Urinalysis - Glucose',NULL,'positive','negative',NULL,NULL,'abnormal','In-house Lab');
INSERT INTO labs VALUES('L_69fcf8b94f','P001','2025-06-20','2025-06-20','33914-3','eGFR',54.0,NULL,'mL/min/1.73m2',60.0,120.0,'low','Quest');
INSERT INTO labs VALUES('L_a7fc7dd259','P001','2025-09-18','2025-09-18','2571-8','Triglycerides',40.52000000000000313,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_d3746ea2f1','P002','2025-02-24','2025-02-24','13457-7','LDL cholesterol (calculated)',21.44000000000000127,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_1c1d07d2b7','P002','2025-12-02','2025-12-02','2823-3','Potassium',4.280000000000000248,NULL,'mmol/L',3.5,5.099999999999999645,'normal','LabCorp');
INSERT INTO labs VALUES('L_459c2f6c56','P002','2025-06-13','2025-06-13','3094-0','BUN',12.5,NULL,'mg/dL',7.0,20.0,'normal','Quest');
INSERT INTO labs VALUES('L_717be7a768','P002','2025-12-03','2025-12-03','2160-0','Creatinine',0.6800000000000000488,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','LabCorp');
INSERT INTO labs VALUES('L_b5719876da','P002','2026-01-10','2026-01-10','718-7','Hemoglobin',14.06000000000000049,NULL,'g/dL',12.0,16.0,'normal','Quest');
INSERT INTO labs VALUES('L_b01faa27c1','P002','2025-11-23','2025-11-23','2345-7','Glucose, random',121.1500000000000056,NULL,'mg/dL',70.0,140.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_1c0193956e','P002','2025-12-30','2025-12-30','2160-0','Creatinine',0.7700000000000000177,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_9e1f4830a9','P002','2025-02-07','2025-02-07','1988-5','CRP',3.069999999999999841,NULL,'mg/L',0.0,10.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_48fb1ac067','P002','2025-04-02','2025-04-02','2093-3','Total cholesterol',72.3299999999999983,NULL,'mg/dL',0.0,200.0,'normal','Quest');
INSERT INTO labs VALUES('L_6ba5746990','P002','2025-10-18','2025-10-18','2571-8','Triglycerides',23.69000000000000127,NULL,'mg/dL',0.0,150.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_fe2e40541d','P002','2025-09-08','2025-09-08','2276-4','Ferritin',-0.4799999999999999823,NULL,'ng/mL',15.0,150.0,'low','Quest');
INSERT INTO labs VALUES('L_af62a879b6','P002','2025-06-20','2025-06-20','1558-6','Glucose, fasting',79.10999999999999944,NULL,'mg/dL',70.0,99.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_0eb6241b89','P002','2025-09-19','2025-09-19','2571-8','Triglycerides',131.3100000000000022,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_ecf05b6fcb','P002','2025-08-13','2025-08-13','13457-7','LDL cholesterol (calculated)',52.49000000000000198,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_647009ca4f','P003','2025-10-20','2025-10-20','2571-8','Triglycerides',111.4399999999999978,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_c318863efd','P003','2025-05-06','2025-05-06','4548-4','Hemoglobin A1c',4.400000000000000356,NULL,'%',4.0,5.599999999999999645,'normal','Quest');
INSERT INTO labs VALUES('L_ae42566bf3','P003','2025-11-26','2025-11-26','3016-3','TSH',2.629999999999999894,NULL,'uIU/mL',0.4000000000000000222,4.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_8e39f5f787','P003','2025-07-02','2025-07-02','35365-6','Vitamin D (25-OH)',30.39000000000000056,NULL,'ng/mL',20.0,50.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_ae397f9167','P003','2025-10-10','2025-10-10','17861-6','Calcium',9.66000000000000014,NULL,'mg/dL',8.599999999999999645,10.19999999999999928,'normal','LabCorp');
INSERT INTO labs VALUES('L_c88a5bbb26','P003','2025-12-23','2025-12-23','2160-0','Creatinine',0.6800000000000000488,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','LabCorp');
INSERT INTO labs VALUES('L_f04cddb2a6','P003','2025-06-13','2025-06-13','2075-0','Chloride',110.8599999999999995,NULL,'mmol/L',98.0,107.0,'high','LabCorp');
INSERT INTO labs VALUES('L_a20bc1d495','P003','2025-12-27','2025-12-27','2160-0','Creatinine',0.7600000000000000088,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','Quest');
INSERT INTO labs VALUES('L_acb308e385','P003','2025-08-04','2025-08-04','2160-0','Creatinine',0.979999999999999983,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_5fffa2f390','P003','2025-09-30','2025-09-30','2160-0','Creatinine',0.6700000000000000399,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','Quest');
INSERT INTO labs VALUES('L_de9e039d9b','P004','2025-02-18','2025-02-18','2093-3','Total cholesterol',210.4499999999999887,NULL,'mg/dL',0.0,200.0,'high','In-house Lab');
INSERT INTO labs VALUES('L_8a79c7887f','P004','2025-12-29','2025-12-29','1558-6','Glucose, fasting',79.84999999999999431,NULL,'mg/dL',70.0,99.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_42c4e42210','P004','2025-04-24','2025-04-24','1558-6','Glucose, fasting',76.5,NULL,'mg/dL',70.0,99.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_48dc1ffb5d','P004','2025-07-04','2025-07-04','2571-8','Triglycerides',101.4800000000000039,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_b43292f8b2','P004','2025-03-09','2025-03-09','2571-8','Triglycerides',20.25,NULL,'mg/dL',0.0,150.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_0cd988519f','P004','2025-06-14','2025-06-14','3016-3','TSH',3.100000000000000088,NULL,'uIU/mL',0.4000000000000000222,4.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_632e9d5a48','P004','2025-05-06','2025-05-06','777-3','Platelets',375.1000000000000227,NULL,'10^3/uL',150.0,450.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_2725743016','P004','2025-02-04','2025-02-04','2085-9','HDL cholesterol',73.0,NULL,'mg/dL',40.0,999.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_f4a39ed30f','P005','2025-11-12','2025-11-12','4548-4','Hemoglobin A1c',5.389999999999999681,NULL,'%',4.0,5.599999999999999645,'normal','Quest');
INSERT INTO labs VALUES('L_c336a7d2b4','P005','2025-12-25','2025-12-25','13457-7','LDL cholesterol (calculated)',60.10000000000000142,NULL,'mg/dL',0.0,100.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_6b9d7c7826','P005','2026-01-18','2026-01-18','2160-0','Creatinine',0.7099999999999999645,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','LabCorp');
INSERT INTO labs VALUES('L_a2fe44d39a','P005','2025-02-16','2025-02-16','2345-7','Glucose, random',118.7600000000000051,NULL,'mg/dL',70.0,140.0,'normal','Quest');
INSERT INTO labs VALUES('L_820b0d37e4','P005','2025-09-06','2025-09-06','4548-4','Hemoglobin A1c',5.849999999999999645,NULL,'%',4.0,5.599999999999999645,'high','Quest');
INSERT INTO labs VALUES('L_2369b95cdc','P005','2025-05-19','2025-05-19','2345-7','Glucose, random',93.0900000000000034,NULL,'mg/dL',70.0,140.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_c54a76d4d0','P005','2025-10-10','2025-10-10','3016-3','TSH',4.589999999999999858,NULL,'uIU/mL',0.4000000000000000222,4.0,'high','LabCorp');
INSERT INTO labs VALUES('L_2dd53db6a6','P005','2025-05-18','2025-05-18','4548-4','Hemoglobin A1c',3.390000000000000124,NULL,'%',4.0,5.599999999999999645,'low','LabCorp');
INSERT INTO labs VALUES('L_13359dc1ed','P005','2025-04-30','2025-04-30','718-7','Hemoglobin',13.89000000000000056,NULL,'g/dL',12.0,16.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a13c5dc49b','P006','2025-05-22','2025-05-22','4548-4','Hemoglobin A1c',6.269999999999999574,NULL,'%',4.0,5.599999999999999645,'high','Quest');
INSERT INTO labs VALUES('L_0875e7442c','P006','2025-12-12','2025-12-12','13457-7','LDL cholesterol (calculated)',21.33999999999999986,NULL,'mg/dL',0.0,100.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_7b1ab1cb0d','P006','2025-11-13','2025-11-13','2160-0','Creatinine',1.020000000000000017,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','Quest');
INSERT INTO labs VALUES('L_7ad2aab3fe','P006','2025-07-17','2025-07-17','718-7','Hemoglobin',11.61999999999999922,NULL,'g/dL',12.0,16.0,'low','In-house Lab');
INSERT INTO labs VALUES('L_50a2d7e510','P006','2025-02-05','2025-02-05','3016-3','TSH',1.629999999999999894,NULL,'uIU/mL',0.4000000000000000222,4.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a6541013fc','P006','2025-08-11','2025-08-11','3016-3','TSH',4.709999999999999965,NULL,'uIU/mL',0.4000000000000000222,4.0,'high','Quest');
INSERT INTO labs VALUES('L_1e951499db','P006','2026-01-13','2026-01-13','13457-7','LDL cholesterol (calculated)',33.18999999999999773,NULL,'mg/dL',0.0,100.0,'normal','Quest');
INSERT INTO labs VALUES('L_22b5769936','P006','2025-03-24','2025-03-24','3016-3','TSH',0.1000000000000000055,NULL,'uIU/mL',0.4000000000000000222,4.0,'low','Quest');
INSERT INTO labs VALUES('L_fcbca9b723','P006','2025-08-26','2025-08-26','2571-8','Triglycerides',32.86999999999999745,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_41eb10ed02','P006','2025-10-14','2025-10-14','2160-0','Creatinine',1.110000000000000098,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','Quest');
INSERT INTO labs VALUES('L_df8d2f545c','P006','2025-03-02','2025-03-02','2276-4','Ferritin',123.0799999999999983,NULL,'ng/mL',15.0,150.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_f46ac87f6a','P006','2025-12-09','2025-12-09','6690-2','WBC',2.810000000000000053,NULL,'10^3/uL',4.0,11.0,'low','LabCorp');
INSERT INTO labs VALUES('L_feca627781','P007','2025-04-13','2025-04-13','4548-4','Hemoglobin A1c',5.929999999999999716,NULL,'%',4.0,5.599999999999999645,'high','Quest');
INSERT INTO labs VALUES('L_13bed8dd5a','P007','2025-09-08','2025-09-08','3016-3','TSH',1.449999999999999956,NULL,'uIU/mL',0.4000000000000000222,4.0,'normal','Quest');
INSERT INTO labs VALUES('L_bb84d94d77','P007','2025-11-19','2025-11-19','1920-8','AST',44.31000000000000227,NULL,'U/L',10.0,40.0,'high','LabCorp');
INSERT INTO labs VALUES('L_f3b4e8e87a','P007','2025-06-03','2025-06-03','2160-0','Creatinine',0.979999999999999983,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_a4d43c0eca','P007','2025-04-10','2025-04-10','2160-0','Creatinine',0.3300000000000000155,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'low','In-house Lab');
INSERT INTO labs VALUES('L_d26cfcbdd2','P007','2025-07-07','2025-07-07','6768-6','Alkaline phosphatase',97.4899999999999949,NULL,'U/L',44.0,147.0,'normal','Quest');
INSERT INTO labs VALUES('L_d5b1490820','P007','2025-05-09','2025-05-09','4548-4','Hemoglobin A1c',5.400000000000000355,NULL,'%',4.0,5.599999999999999645,'normal','In-house Lab');
INSERT INTO labs VALUES('L_03fbc8a615','P007','2025-03-03','2025-03-03','2093-3','Total cholesterol',155.7800000000000011,NULL,'mg/dL',0.0,200.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_9dc29ac1e4','P007','2025-07-07','2025-07-07','13457-7','LDL cholesterol (calculated)',45.6700000000000017,NULL,'mg/dL',0.0,100.0,'normal','Quest');
INSERT INTO labs VALUES('L_052e603f2a','P007','2026-01-08','2026-01-08','1988-5','CRP',13.93999999999999951,NULL,'mg/L',0.0,10.0,'high','LabCorp');
INSERT INTO labs VALUES('L_736c2c47dc','P007','2025-07-03','2025-07-03','2345-7','Glucose, random',128.9799999999999898,NULL,'mg/dL',70.0,140.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_33e63287c8','P007','2025-09-14','2025-09-14','1975-2','Total bilirubin',0.4099999999999999756,NULL,'mg/dL',0.1000000000000000055,1.199999999999999956,'normal','In-house Lab');
INSERT INTO labs VALUES('L_5ef259f7cc','P007','2025-11-25','2025-11-25','3024-7','Free T4',1.479999999999999983,NULL,'ng/dL',0.8000000000000000444,1.800000000000000044,'normal','LabCorp');
INSERT INTO labs VALUES('L_6d6db6289f','P007','2025-05-30','2025-05-30','2888-6','Urinalysis - Protein',NULL,'negative','negative/trace',NULL,NULL,'normal','LabCorp');
INSERT INTO labs VALUES('L_e867d5c489','P008','2025-09-22','2025-09-22','13457-7','LDL cholesterol (calculated)',13.00999999999999979,NULL,'mg/dL',0.0,100.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_8abf19004d','P008','2025-03-05','2025-03-05','13457-7','LDL cholesterol (calculated)',60.89999999999999858,NULL,'mg/dL',0.0,100.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_594b3dab40','P008','2025-12-14','2025-12-14','2160-0','Creatinine',1.199999999999999956,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_adbbb21c54','P008','2025-03-18','2025-03-18','13457-7','LDL cholesterol (calculated)',149.8400000000000034,NULL,'mg/dL',0.0,100.0,'high','Quest');
INSERT INTO labs VALUES('L_8d38331010','P008','2025-09-17','2025-09-17','2888-6','Urinalysis - Protein',NULL,'trace','negative/trace',NULL,NULL,'normal','LabCorp');
INSERT INTO labs VALUES('L_0f11227d30','P008','2026-01-05','2026-01-05','13457-7','LDL cholesterol (calculated)',66.37000000000000454,NULL,'mg/dL',0.0,100.0,'normal','Quest');
INSERT INTO labs VALUES('L_7a0597bf7d','P008','2025-05-09','2025-05-09','13457-7','LDL cholesterol (calculated)',61.77000000000000312,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_44bc10e9b4','P008','2025-06-16','2025-06-16','2571-8','Triglycerides',42.21000000000000085,NULL,'mg/dL',0.0,150.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_d1094124c3','P008','2025-06-18','2025-06-18','718-7','Hemoglobin',13.66999999999999993,NULL,'g/dL',12.0,16.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_e6c6593833','P008','2025-05-06','2025-05-06','6690-2','WBC',2.060000000000000053,NULL,'10^3/uL',4.0,11.0,'low','In-house Lab');
INSERT INTO labs VALUES('L_49a0f51775','P008','2025-08-21','2025-08-21','2075-0','Chloride',96.0300000000000011,NULL,'mmol/L',98.0,107.0,'low','Quest');
INSERT INTO labs VALUES('L_1e65fffbc5','P008','2025-12-22','2025-12-22','2571-8','Triglycerides',32.57000000000000028,NULL,'mg/dL',0.0,150.0,'normal','Quest');
INSERT INTO labs VALUES('L_e2eabbdb1d','P008','2025-03-20','2025-03-20','4548-4','Hemoglobin A1c',5.719999999999999752,NULL,'%',4.0,5.599999999999999645,'high','Quest');
INSERT INTO labs VALUES('L_8eef86bddd','P008','2025-08-12','2025-08-12','2888-6','Urinalysis - Protein',NULL,'positive','negative/trace',NULL,NULL,'abnormal','In-house Lab');
INSERT INTO labs VALUES('L_9aa3f68098','P009','2025-10-14','2025-10-14','17861-6','Calcium',8.47000000000000064,NULL,'mg/dL',8.599999999999999645,10.19999999999999928,'low','Quest');
INSERT INTO labs VALUES('L_fe3982b1a0','P009','2025-07-12','2025-07-12','1920-8','AST',23.62000000000000099,NULL,'U/L',10.0,40.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_6518fc5228','P009','2025-12-09','2025-12-09','2160-0','Creatinine',1.209999999999999965,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_8259c005ba','P009','2025-10-05','2025-10-05','777-3','Platelets',364.5,NULL,'10^3/uL',150.0,450.0,'normal','Quest');
INSERT INTO labs VALUES('L_901f691efa','P009','2025-12-06','2025-12-06','6768-6','Alkaline phosphatase',169.4300000000000068,NULL,'U/L',44.0,147.0,'high','In-house Lab');
INSERT INTO labs VALUES('L_c944d9710d','P009','2025-05-22','2025-05-22','2571-8','Triglycerides',212.3000000000000113,NULL,'mg/dL',0.0,150.0,'high','In-house Lab');
INSERT INTO labs VALUES('L_c982d3491f','P009','2025-12-18','2025-12-18','3016-3','TSH',0.939999999999999947,NULL,'uIU/mL',0.4000000000000000222,4.0,'normal','In-house Lab');
INSERT INTO labs VALUES('L_74496726d4','P009','2025-03-15','2025-03-15','2888-6','Urinalysis - Protein',NULL,'trace','negative/trace',NULL,NULL,'normal','Quest');
INSERT INTO labs VALUES('L_2ea1e970e7','P010','2025-12-28','2025-12-28','1558-6','Glucose, fasting',89.53000000000000113,NULL,'mg/dL',70.0,99.0,'normal','Quest');
INSERT INTO labs VALUES('L_4358dffda0','P010','2026-01-18','2026-01-18','2028-9','CO2 (Bicarbonate)',26.03999999999999915,NULL,'mmol/L',22.0,29.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_a492bf568d','P010','2026-01-07','2026-01-07','2345-7','Glucose, random',83.01000000000000511,NULL,'mg/dL',70.0,140.0,'normal','LabCorp');
INSERT INTO labs VALUES('L_8adbafac89','P010','2025-07-06','2025-07-06','777-3','Platelets',399.25,NULL,'10^3/uL',150.0,450.0,'normal','Quest');
INSERT INTO labs VALUES('L_b917cdd4b3','P010','2025-10-18','2025-10-18','3016-3','TSH',0.1100000000000000005,NULL,'uIU/mL',0.4000000000000000222,4.0,'low','LabCorp');
INSERT INTO labs VALUES('L_3b2dde7ab8','P010','2025-05-29','2025-05-29','2160-0','Creatinine',1.110000000000000098,NULL,'mg/dL',0.5999999999999999778,1.300000000000000044,'normal','In-house Lab');
INSERT INTO labs VALUES('L_31df1d6b27','P010','2025-10-30','2025-10-30','1920-8','AST',41.96000000000000085,NULL,'U/L',10.0,40.0,'high','In-house Lab');
INSERT INTO labs VALUES('L_5d8cbb5589','P010','2025-11-27','2025-11-27','2888-6','Urinalysis - Protein',NULL,'negative','negative/trace',NULL,NULL,'normal','Quest');
INSERT INTO labs VALUES('L_50a1a05fae','P010','2025-12-01','2025-12-01','2951-2','Sodium',143.9099999999999966,NULL,'mmol/L',135.0,145.0,'normal','Quest');
INSERT INTO labs VALUES('L_a488751471','P010','2025-06-20','2025-06-20','13457-7','LDL cholesterol (calculated)',81.29999999999999716,NULL,'mg/dL',0.0,100.0,'normal','In-house Lab');
CREATE TABLE medications (
  med_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL,
  rxnorm_code TEXT,
  med_name TEXT NOT NULL,
  dose TEXT,
  route TEXT,
  frequency TEXT,
  start_date TEXT NOT NULL,
  end_date TEXT,
  status TEXT CHECK (status IN ('active','stopped')) NOT NULL,
  indication TEXT,
  prescriber_specialty TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
INSERT INTO medications VALUES('M_3489ef713f','P001','860975','Metformin','500 mg','oral','twice daily','2023-10-27',NULL,'active','Type 2 diabetes','Primary Care');
INSERT INTO medications VALUES('M_61e0b67cc0','P002','29046','Lisinopril','10 mg','oral','once daily','2023-09-30',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_e3633584e4','P003','17767','Amlodipine','5 mg','oral','once daily','2025-07-29',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_e02da80abc','P004','83367','Atorvastatin','20 mg','oral','once daily','2025-02-03',NULL,'active','Hyperlipidemia','Primary Care');
INSERT INTO medications VALUES('M_7d1f440f9e','P005','36567','Simvastatin','20 mg','oral','once daily','2024-04-29',NULL,'active','Hyperlipidemia','Primary Care');
INSERT INTO medications VALUES('M_792a11d6b0','P006','10582','Levothyroxine','75 mcg','oral','once daily','2025-03-15',NULL,'active','Hypothyroidism','Endocrinology');
INSERT INTO medications VALUES('M_822641ba6c','P007','7646','Omeprazole','20 mg','oral','once daily','2025-05-11',NULL,'active','GERD','Primary Care');
INSERT INTO medications VALUES('M_066f3e64ba','P008','435','Albuterol inhaler','90 mcg','inhalation','as needed','2025-05-24',NULL,'active','Asthma','Pulmonology');
INSERT INTO medications VALUES('M_f6cb5a97b6','P009','36437','Sertraline','50 mg','oral','once daily','2025-06-26',NULL,'active','Depression/anxiety','Psychiatry');
INSERT INTO medications VALUES('M_41b5fe3048','P010','4493','Fluoxetine','20 mg','oral','once daily','2024-04-17',NULL,'active','Depression','Psychiatry');
INSERT INTO medications VALUES('M_76d5138b24','P001','5487','Hydrochlorothiazide','12.5 mg','oral','once daily','2025-09-25',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_73079cfffe','P002','52175','Losartan','50 mg','oral','once daily','2025-03-24',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_3ca589a09e','P003','25480','Gabapentin','300 mg','oral','at bedtime','2025-04-08',NULL,'active','Neuropathic pain','Neurology');
INSERT INTO medications VALUES('M_024b80f6a8','P004','723','Amoxicillin','500 mg','oral','three times daily','2025-08-20',NULL,'active','Acute infection','Urgent Care');
INSERT INTO medications VALUES('M_dd3d2acf7b','P005','18631','Azithromycin','250 mg','oral','daily (5-day course)','2025-10-24',NULL,'active','Respiratory infection','Urgent Care');
INSERT INTO medications VALUES('M_332c1c9db0','P006','161','Acetaminophen','500 mg','oral','every 6 hours as needed','2024-08-01','2026-01-05','stopped','Pain/fever','Primary Care');
INSERT INTO medications VALUES('M_df05bde7ff','P007','5640','Ibuprofen','400 mg','oral','every 6 hours as needed','2024-08-28','2026-01-17','stopped','Pain/inflammation','Primary Care');
INSERT INTO medications VALUES('M_6970a032c8','P008','11289','Warfarin','5 mg','oral','once daily','2025-02-03',NULL,'active','Anticoagulation','Cardiology');
INSERT INTO medications VALUES('M_6576a73165','P009','1364434','Apixaban','5 mg','oral','twice daily','2025-10-10',NULL,'active','Atrial fibrillation','Cardiology');
INSERT INTO medications VALUES('M_d4301b91a5','P010','32968','Clopidogrel','75 mg','oral','once daily','2024-04-12',NULL,'active','Antiplatelet therapy','Cardiology');
INSERT INTO medications VALUES('M_17695f8399','P001','274783','Insulin glargine','10 units','subcutaneous','nightly','2025-09-15',NULL,'active','Diabetes','Endocrinology');
INSERT INTO medications VALUES('M_936feabba7','P002','20610','Cetirizine','10 mg','oral','once daily','2025-06-01',NULL,'active','Allergic rhinitis','Primary Care');
INSERT INTO medications VALUES('M_42f927c558','P003','87636','Fexofenadine','180 mg','oral','once daily','2025-03-09',NULL,'active','Allergic rhinitis','Primary Care');
INSERT INTO medications VALUES('M_ec1a7d174a','P004','8640','Prednisone','20 mg','oral','daily (short course)','2024-01-20','2026-01-13','stopped','Inflammation','Urgent Care');
INSERT INTO medications VALUES('M_26dcd9ff15','P005','3640','Doxycycline','100 mg','oral','twice daily','2024-02-17',NULL,'active','Infection','Urgent Care');
INSERT INTO medications VALUES('M_1abfe2da92','P006','77492','Tamsulosin','0.4 mg','oral','once daily','2024-03-06',NULL,'active','BPH','Urology');
INSERT INTO medications VALUES('M_e9f9112de1','P007','866429','Metoprolol succinate','25 mg','oral','once daily','2025-10-23',NULL,'active','Hypertension/Rate control','Cardiology');
INSERT INTO medications VALUES('M_3f487b1be5','P008','4603','Furosemide','20 mg','oral','once daily','2025-07-09',NULL,'active','Edema/Heart failure','Cardiology');
INSERT INTO medications VALUES('M_298bac013b','P009','88249','Montelukast','10 mg','oral','once daily','2025-03-14',NULL,'active','Asthma/allergies','Pulmonology');
INSERT INTO medications VALUES('M_aa065e735b','P010','4917','Nitroglycerin SL','0.4 mg','sublingual','as needed chest pain','2023-11-12',NULL,'active','Angina','Cardiology');
INSERT INTO medications VALUES('M_7493e22afc','P001','77492','Tamsulosin','0.4 mg','oral','once daily','2024-10-19',NULL,'active','BPH','Urology');
INSERT INTO medications VALUES('M_cb6ed87d3d','P002','7646','Omeprazole','20 mg','oral','once daily','2024-08-16',NULL,'active','GERD','Primary Care');
INSERT INTO medications VALUES('M_69cf09e268','P002','83367','Atorvastatin','20 mg','oral','once daily','2025-07-20',NULL,'active','Hyperlipidemia','Primary Care');
INSERT INTO medications VALUES('M_fa83d630ab','P002','36437','Sertraline','50 mg','oral','once daily','2024-05-15',NULL,'active','Depression/anxiety','Psychiatry');
INSERT INTO medications VALUES('M_b451bbfc45','P003','4493','Fluoxetine','20 mg','oral','once daily','2025-09-03','2025-12-11','stopped','Depression','Psychiatry');
INSERT INTO medications VALUES('M_70c9ba9e6f','P003','18631','Azithromycin','250 mg','oral','daily (5-day course)','2023-12-27',NULL,'active','Respiratory infection','Urgent Care');
INSERT INTO medications VALUES('M_8116c4dd7e','P003','11289','Warfarin','5 mg','oral','once daily','2025-06-19',NULL,'active','Anticoagulation','Cardiology');
INSERT INTO medications VALUES('M_1c394d094b','P004','10582','Levothyroxine','75 mcg','oral','once daily','2024-05-16',NULL,'active','Hypothyroidism','Endocrinology');
INSERT INTO medications VALUES('M_c46dc14be9','P005','11289','Warfarin','5 mg','oral','once daily','2025-07-22',NULL,'active','Anticoagulation','Cardiology');
INSERT INTO medications VALUES('M_4facf5f49d','P005','17767','Amlodipine','5 mg','oral','once daily','2024-11-21',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_afd928e0d4','P006','7646','Omeprazole','20 mg','oral','once daily','2025-09-24',NULL,'active','GERD','Primary Care');
INSERT INTO medications VALUES('M_258d2729ee','P006','4603','Furosemide','20 mg','oral','once daily','2024-03-15',NULL,'active','Edema/Heart failure','Cardiology');
INSERT INTO medications VALUES('M_d29466d951','P006','5487','Hydrochlorothiazide','12.5 mg','oral','once daily','2025-06-21',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_1e87c4542a','P007','32968','Clopidogrel','75 mg','oral','once daily','2024-02-18','2025-12-22','stopped','Antiplatelet therapy','Cardiology');
INSERT INTO medications VALUES('M_05f45469b2','P007','8640','Prednisone','20 mg','oral','daily (short course)','2024-05-11',NULL,'active','Inflammation','Urgent Care');
INSERT INTO medications VALUES('M_fa5ba417f5','P007','20610','Cetirizine','10 mg','oral','once daily','2023-12-26','2026-01-13','stopped','Allergic rhinitis','Primary Care');
INSERT INTO medications VALUES('M_20a6480f6a','P007','18631','Azithromycin','250 mg','oral','daily (5-day course)','2025-03-17','2025-12-10','stopped','Respiratory infection','Urgent Care');
INSERT INTO medications VALUES('M_f1e2b7eb13','P008','29046','Lisinopril','10 mg','oral','once daily','2023-10-27',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_7ad2432886','P008','32968','Clopidogrel','75 mg','oral','once daily','2025-07-01',NULL,'active','Antiplatelet therapy','Cardiology');
INSERT INTO medications VALUES('M_0913d902c0','P008','5640','Ibuprofen','400 mg','oral','every 6 hours as needed','2024-02-29',NULL,'active','Pain/inflammation','Primary Care');
INSERT INTO medications VALUES('M_31d0872c5d','P009','11289','Warfarin','5 mg','oral','once daily','2025-06-21',NULL,'active','Anticoagulation','Cardiology');
INSERT INTO medications VALUES('M_24f7d4bdcd','P009','52175','Losartan','50 mg','oral','once daily','2023-09-02',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_82a47ce5e8','P009','5487','Hydrochlorothiazide','12.5 mg','oral','once daily','2025-07-01',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_6335665483','P009','17767','Amlodipine','5 mg','oral','once daily','2025-09-26',NULL,'active','Hypertension','Primary Care');
INSERT INTO medications VALUES('M_782f4281c2','P010','36567','Simvastatin','20 mg','oral','once daily','2024-03-13',NULL,'active','Hyperlipidemia','Primary Care');
INSERT INTO medications VALUES('M_5688d37e0b','P010','18631','Azithromycin','250 mg','oral','daily (5-day course)','2025-05-13',NULL,'active','Respiratory infection','Urgent Care');
CREATE TABLE allergies (
  allergy_id TEXT PRIMARY KEY,
  patient_id TEXT NOT NULL,
  substance TEXT NOT NULL,
  reaction TEXT NOT NULL,
  severity TEXT CHECK (severity IN ('mild','moderate','severe')) NOT NULL,
  recorded_date TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
INSERT INTO allergies VALUES('A_572acb8ba7','P001','Shellfish','Hives','moderate','2022-08-17');
INSERT INTO allergies VALUES('A_d9ce5ce7c8','P002','Aspirin','Hives','moderate','2021-11-25');
INSERT INTO allergies VALUES('A_705ea2cea7','P003','Iodinated contrast','Itching','moderate','2024-07-21');
INSERT INTO allergies VALUES('A_0329bf1aaa','P004','Sulfonamide antibiotics','Hives','moderate','2023-11-07');
INSERT INTO allergies VALUES('A_d34af23e50','P005','Ibuprofen','Wheezing','severe','2021-07-09');
INSERT INTO allergies VALUES('A_cb0615e5dd','P006','Latex','Contact dermatitis','mild','2020-10-18');
INSERT INTO allergies VALUES('A_447bbab60b','P007','Ibuprofen','Wheezing','severe','2025-01-30');
INSERT INTO allergies VALUES('A_e3df69b9a1','P008','Ibuprofen','Wheezing','severe','2024-07-19');
INSERT INTO allergies VALUES('A_4616d6f3d8','P008','Sulfonamide antibiotics','Hives','moderate','2024-01-25');
INSERT INTO allergies VALUES('A_6da965b18c','P009','Shellfish','Hives','moderate','2021-12-03');
INSERT INTO allergies VALUES('A_44f6b99a9c','P009','Milk','GI upset','mild','2021-04-30');
INSERT INTO allergies VALUES('A_c84d59c2ba','P010','Egg','Rash','mild','2021-07-17');
INSERT INTO allergies VALUES('A_9d5e3a6698','P010','Aspirin','Hives','moderate','2021-09-21');
INSERT INTO allergies VALUES('A_8685d3ad34','P007','Penicillin','Rash','moderate','2021-09-08');
INSERT INTO allergies VALUES('A_d0b3a145d9','P009','Peanuts','Anaphylaxis','severe','2024-01-17');
COMMIT;

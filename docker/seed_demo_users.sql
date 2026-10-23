-- Suppress first-login Product Registration & Telemetry modal
DELETE FROM product_registration;
INSERT INTO product_registration (email, opt_out, telemetry_disabled, last_ask_version)
VALUES (NULL, 1, 1, '8.4.1');

-- Create demo users (clinician=5, physician=6 [Donna Lee], receptionist=7, accountant=8)
DELETE FROM users WHERE id IN (5, 6, 7, 8);
INSERT INTO users (
    id, username, password, authorized, fname, lname,
    facility, facility_id, see_auth, active, cal_ui,
    taxonomy, calendar, abook_type, default_warehouse, irnpool,
    main_menu_role, patient_menu_role, portal_user, supervisor_id, billing_facility_id
) VALUES
(5, 'clinician', 'NoLongerUsed', 1, 'Fred', 'Stone', 'Your Clinic Name Here', 3, 1, 1, 3, '207Q00000X', 1, '', '', '', 'standard', 'standard', 0, 0, 0),
(6, 'physician', 'NoLongerUsed', 1, 'Donna', 'Lee', 'Your Clinic Name Here', 3, 1, 1, 3, '207Q00000X', 1, '', '', '', 'standard', 'standard', 0, 0, 0),
(7, 'receptionist', 'NoLongerUsed', 0, 'Barbara', 'Wallace', 'Your Clinic Name Here', 3, 1, 1, 3, '207Q00000X', 0, '', '', '', 'standard', 'standard', 0, 0, 0),
(8, 'accountant', 'NoLongerUsed', 0, 'Ernie', 'Stent', 'Your Clinic Name Here', 3, 1, 1, 3, '207Q00000X', 0, '', '', '', 'standard', 'standard', 0, 0, 0);

-- Set demo passwords (clinician/clinician, physician/physician, receptionist/receptionist, accountant/accountant)
DELETE FROM users_secure WHERE id IN (5, 6, 7, 8);
INSERT INTO users_secure (id, username, password, last_update_password) VALUES
(5, 'clinician', '$2y$12$jNZzHR2/yVNJ4gWnqNDQ0eTOBzLZrb1ksucoggM9QE3Bw0tE3Daf2', NOW()),
(6, 'physician', '$2y$12$CO76dkZiUiVx/JGBm.8fteIAfcvngaROBgAhahVtJrD.hIEX20WD.', NOW()),
(7, 'receptionist', '$2y$12$9XW3KuKAiD7FsixGbkAruOqQS3KoRSnyw7DAx71cdt2EX3V7KwQVC', NOW()),
(8, 'accountant', '$2y$12$AW7rfDpm.xWIqf/wB290A.wzzDGD6WWjKMkU30hA8.TY9BQ4OvAt.', NOW());

-- Assign facility group
DELETE FROM groups WHERE user IN ('clinician', 'physician', 'receptionist', 'accountant');
INSERT INTO groups (name, user) VALUES
('Default', 'clinician'),
('Default', 'physician'),
('Default', 'receptionist'),
('Default', 'accountant');

-- Assign GACL roles (12=Clinicians, 13=Physicians, 14=Front Office, 15=Accounting)
DELETE FROM gacl_aro WHERE id IN (12, 13, 14, 15);
INSERT INTO gacl_aro (id, section_value, value, order_value, name, hidden) VALUES
(12, 'users', 'clinician', 10, 'Fred Stone', 0),
(13, 'users', 'physician', 10, 'Donna Lee', 0),
(14, 'users', 'receptionist', 10, 'Barbara Wallace', 0),
(15, 'users', 'accountant', 10, 'Ernie Stent', 0);

DELETE FROM gacl_groups_aro_map WHERE aro_id IN (12, 13, 14, 15);
INSERT INTO gacl_groups_aro_map (group_id, aro_id) VALUES
(12, 12),
(13, 13),
(14, 14),
(15, 15);

UPDATE gacl_aro_seq SET id = 15;

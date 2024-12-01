INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_superuser, is_active, date_joined)
VALUES
('manager1', 'John', 'Doe', 'manager1@company.com', 'pbkdf2_sha256$870000$k4wuuImcedpvkFhNWN16NL$oKAw5oadebgj1E9KMMQLN1TCw0uQkf/Z70GIMfxyt6c=', TRUE, TRUE, TRUE, '2024-01-01'),
('staff2', 'Tom', 'Brown', 'staff2@company.com', 'pbkdf2_sha256$870000$k4wuuImcedpvkFhNWN16NL$oKAw5oadebgj1E9KMMQLN1TCw0uQkf/Z70GIMfxyt6c=', FALSE, FALSE, TRUE, '2024-01-01'),
('staff3', 'Emily', 'Clark', 'staff3@company.com', 'pbkdf2_sha256$870000$k4wuuImcedpvkFhNWN16NL$oKAw5oadebgj1E9KMMQLN1TCw0uQkf/Z70GIMfxyt6c=', FALSE, FALSE, TRUE, '2024-01-01'),
('staff4', 'Michael', 'Johnson', 'staff4@company.com', 'pbkdf2_sha256$870000$k4wuuImcedpvkFhNWN16NL$oKAw5oadebgj1E9KMMQLN1TCw0uQkf/Z70GIMfxyt6c=', FALSE, FALSE, TRUE, '2024-01-01'),
('staff1', 'Jane', 'Smith', 'staff1@company.com', 'pbkdf2_sha256$870000$k4wuuImcedpvkFhNWN16NL$oKAw5oadebgj1E9KMMQLN1TCw0uQkf/Z70GIMfxyt6c=', FALSE, FALSE, TRUE, '2024-01-01');

INSERT INTO core_employee (user_id, role, start_date, remaining_leaves)
VALUES
(2, 'MANAGER', '2023-01-01', 15),
(3, 'STAFF', '2023-06-01', 10),
(4, 'STAFF', '2023-09-01', 5),
(5, 'STAFF', '2023-02-01', 12),
(6, 'STAFF', '2023-03-01', 8);

INSERT INTO core_leaverequest (employee_id, leave_type, start_date, end_date, reason, status, requested_at, updated_at)
VALUES
(2, 'ANNUAL', '2024-12-05', '2024-12-10', 'Family vacation', 'APPROVED', '2024-11-20', '2024-11-21'),
(3, 'SICK', '2024-12-01', '2024-12-02', 'Medical reasons', 'PENDING', '2024-11-29', '2024-11-30'),
(2, 'PERSONAL', '2024-12-12', '2024-12-13', 'Personal matters', 'REJECTED', '2024-11-25', '2024-11-26'),
(4, 'ANNUAL', '2024-11-10', '2024-11-12', 'Travel', 'APPROVED', '2024-11-01', '2024-11-02'),
(5, 'SICK', '2024-12-15', '2024-12-16', 'Flu', 'APPROVED', '2024-11-30', '2024-12-01'),
(3, 'ANNUAL', '2024-12-20', '2024-12-25', 'Holiday', 'PENDING', '2024-12-01', '2024-12-02');

INSERT INTO core_checkinout (employee_id, check_in_time, check_out_time, late_minutes)
VALUES
(2, '2024-12-01 08:10:00', '2024-12-01 17:00:00', 10),
(3, '2024-12-01 08:30:00', '2024-12-01 17:05:00', 0),
(4, '2024-12-01 09:15:00', '2024-12-01 18:00:00', 45),
(5, '2024-12-01 08:50:00', '2024-12-01 17:20:00', 20),
(2, '2024-12-02 08:05:00', '2024-12-02 17:00:00', 5),
(3, '2024-12-02 08:40:00', '2024-12-02 16:55:00', 10),
(4, '2024-12-02 09:00:00', '2024-12-02 17:30:00', 30),
(5, '2024-12-02 08:55:00', '2024-12-02 17:15:00', 15);

INSERT INTO core_notification (recipient_id, message, created_at, is_read, role)
VALUES
(2, 'Your leave request has been approved.', '2024-11-21', TRUE, 'MANAGER'),
(3, 'Your leave request is pending review.', '2024-11-30', FALSE, 'STAFF'),
(2, 'You have accumulated 40 minutes of late time this week.', '2024-12-01', FALSE, 'MANAGER'),
(4, 'Your leave request has been approved.', '2024-11-12', TRUE, 'STAFF'),
(5, 'Your leave request has been approved.', '2024-12-01', TRUE, 'STAFF'),
(1, 'Staff member Jane Smith has a pending leave request.', '2024-12-01', FALSE, 'MANAGER'),
(1, 'Staff member Emily Clark has accumulated 1 hour late today.', '2024-12-02', FALSE, 'MANAGER');

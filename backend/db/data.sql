-- 1. Create group
INSERT INTO groups (name, description, password, num_preferences, direct_matches, additional_prefs_allowed, match_complete)
VALUES ('Team Alpha', 'Group of 15 members for matching', 'securepass', 3, FALSE, FALSE, FALSE),
('Team Beta', 'Group of 4 members for matching', 'securepass', 3, TRUE, FALSE, FALSE);

-- 2. Create tasks with assignment count ranges
-- Assumes the group ID of 'Team Alpha' is 1
INSERT INTO tasks (group_id, name, description, group_task_id, min_assignment_count, max_assignment_count)
VALUES 
(1, 'Design Document', 'Write the project design documentation', 0, 5, 7),
(1, 'Prototype Build', 'Build a prototype of the solution', 1, 5, 5),
(1, 'Final Report', 'Prepare and submit the final report', 2, 2, 5),
(2, 'Design Document', 'Write the project design documentation', 0, 1, 1),
(2, 'Prototype Build', 'Build a prototype of the solution', 1, 1, 1),
(2, 'Final Report', 'Prepare and submit the final report', 2, 1, 1),
(2, 'Team Lead', 'Manage communications & lead team', 3, 1, 1);

INSERT INTO user_accounts (id, email, hashed_password, name, is_admin, is_deleted)
VALUES
(1, 'ava.johnson@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Ava Johnson', FALSE, FALSE),
(2, 'liam.smith@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Liam Smith', FALSE, FALSE),
(3, 'olivia.chen@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Olivia Chen', FALSE, FALSE),
(4, 'noah.martinez@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Noah Martinez', FALSE, FALSE),
(5, 'emma.patel@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Emma Patel', FALSE, FALSE),
(6, 'james.kim@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'James Kim', FALSE, FALSE),
(7, 'sophia.nguyen@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Sophia Nguyen', FALSE, FALSE),
(8, 'benjamin.lee@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Benjamin Lee', FALSE, FALSE),
(9, 'mia.garcia@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Mia Garcia', FALSE, FALSE),
(10, 'lucas.anderson@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Lucas Anderson', FALSE, FALSE),
(11, 'isabella.thomas@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Isabella Thomas', FALSE, FALSE),
(12, 'henry.davis@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Henry Davis', FALSE, FALSE),
(13, 'charlotte.wilson@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Charlotte Wilson', FALSE, FALSE),
(14, 'elijah.moore@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Elijah Moore', FALSE, FALSE),
(15, 'amelia.clark@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Amelia Clark', FALSE, FALSE),
(16, 'sarah.green@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Sarah Green', FALSE, FALSE),
(17, 'ben.fravel@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Ben Fravel', FALSE, FALSE),
(18, 'owen.lowrey@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Owen Lowrey', FALSE, FALSE),
(19, 'nick.swenson@example.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Nick Swenson', FALSE, FALSE),
(20, 'martha.s@email.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Martha Stewart', TRUE),
(21, 'bhealy@email.com', '$2b$12$7XAU3MgjV/EgdqfuCijg5e3/9CmVepLmRnRZu50axlqfgVrf2KdfG', 'Byron Healy', TRUE);


INSERT INTO group_members (group_id, group_member_id, account_id, is_deleted)
VALUES
(1, 0, 1, FALSE),
(1, 1, 2, FALSE),
(1, 2, 3, FALSE),
(1, 3, 4, FALSE),
(1, 4, 5, FALSE),
(1, 5, 6, FALSE),
(1, 6, 7, FALSE),
(1, 7, 8, FALSE),
(1, 8, 9, FALSE),
(1, 9, 10, FALSE),
(1, 10, 11, FALSE),
(1, 11, 12, FALSE),
(1, 12, 13, FALSE),
(1, 13, 14, FALSE),
(1, 14, 15, FALSE),
(2, 0, 16, FALSE),
(2, 1, 17, FALSE),
(2, 2, 18, FALSE),
(2, 3, 19, FALSE),
(1, null, 20, FALSE),
(2, null, 21, FALSE);


-- 4. Insert preferences (member_id 1-15; task_id 1-3)
INSERT INTO task_preferences (member_id, task_id, rank) VALUES
(1, 1, 0), (1, 2, 1), (1, 3, 2),
(2, 2, 0), (2, 3, 1), (2, 1, 2),
(3, 1, 0), (3, 3, 1), (3, 2, 2),
(4, 2, 0), (4, 3, 1), (4, 1, 2),
(5, 1, 0), (5, 2, 1), (5, 3, 2),
(6, 1, 0), (6, 3, 1), (6, 2, 2),
(7, 3, 0), (7, 1, 1), (7, 2, 2),
(8, 2, 0), (8, 1, 1), (8, 3, 2),
(9, 1, 0), (9, 2, 1), (9, 3, 2),
(10, 2, 0), (10, 3, 1), (10, 1, 2),
(11, 1, 0), (11, 3, 1), (11, 2, 2),
(12, 2, 0), (12, 1, 1), (12, 3, 2),
(13, 1, 0), (13, 2, 1), (13, 3, 2),
(14, 3, 0), (14, 1, 1), (14, 2, 2),
(15, 2, 0), (15, 3, 1), (15, 1, 2),
(16, 4, 0), (16, 5, 1), (16, 7, 2),
(17, 7, 0), (17, 5, 1), (17, 6, 2),
(18, 5, 0), (18, 4, 1), (18, 7, 2),
(19, 7, 0), (19, 4, 1), (19, 6, 2);

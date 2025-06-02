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

-- 3. Create 15 members with names
INSERT INTO group_members (group_id, is_admin, name, group_member_id)
VALUES 
(1, FALSE, 'Ava Johnson', 0),
(1, FALSE, 'Liam Smith', 1),
(1, FALSE, 'Olivia Chen', 2),
(1, FALSE, 'Noah Martinez', 3),
(1, FALSE, 'Emma Patel', 4),
(1, FALSE, 'James Kim', 5),
(1, FALSE, 'Sophia Nguyen', 6),
(1, FALSE, 'Benjamin Lee', 7),
(1, FALSE, 'Mia Garcia', 8),
(1, FALSE, 'Lucas Anderson', 9),
(1, FALSE, 'Isabella Thomas', 10),
(1, FALSE, 'Henry Davis', 11),
(1, FALSE, 'Charlotte Wilson', 12),
(1, FALSE, 'Elijah Moore', 13),
(1, FALSE, 'Amelia Clark', 14),
(2, FALSE, 'Sarah Green', 0),
(2, FALSE, 'Ben Fravel', 1),
(2, FALSE, 'Owen Lowrey', 2),
(2, FALSE, 'Nick Swenson', 3);


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

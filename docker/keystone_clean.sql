
USE keystone

DELETE FROM user_group_membership;

DELETE FROM keystone.group;

DELETE FROM project WHERE name LIKE 'shield%';

DELETE FROM user WHERE extra NOT LIKE '{}';

DELETE FROM role WHERE name LIKE 'shield%';

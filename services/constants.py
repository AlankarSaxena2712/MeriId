USER_ROLE = (
    ('operator', 'Operator'),
    ('user', 'User'),
    ('admin', 'Admin'),
)

RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

USER_STATUS = (
    ('active', 'Active'),
    ('kyc', 'Kyc'),
    ('other', 'Other'),
    ('pan', 'Pan'),
    ('aadhar', 'Aadhar'),
    ('video', 'Video'),
    ('pending', "Pending"),
    ('disabled', 'Disabled'),
)

BOOKING_STATUS = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('completed', 'completed'),
)

ATTENDANCE_STATUS = (
    ('present', 'present'),
    ('absent', 'absent'),
)

BOOKING_SLOT_TIME = (
    ('10_to_11', '10_to_11'),
    ('11_to_12', '11_to_12'),
    ('12_to_1', '12_to_1'),
    ('1_to_2', '1_to_2'),
    ('2_to_3', '2_to_3'),
    ('3_to_4', '3_to_4'),
    ('4_to_5', '4_to_5'),
    ('5_to_6', '5_to_6'),
)

BOOKING_TYPE = (
    ('create', 'create'),
    ('update', 'update'),
)
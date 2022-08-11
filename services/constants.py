USER_ROLE = (
    ('operator', 'Operator'),
    ('user', 'User'),
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
)

BOOKING_STATUS = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
)

ATTENDANCE_STATUS = (
    ('present', 'present'),
    ('absent', 'absent'),
)
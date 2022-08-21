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
    ('operator_out', 'operator_out'),
)

ATTENDANCE_STATUS = (
    ('present', 'present'),
    ('absent', 'absent'),
    ('done', 'done'),
)

BOOKING_SLOT_TIME = (
    ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
    ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
    ('12:00 PM - 1:00 PM', '12:00 PM - 1:00 PM'),
    ('1:00 PM - 2:00 PM', '1:00 PM - 2:00 PM'),
    ('2:00 PM - 3:00 PM', '2:00 PM - 3:00 PM'),
    ('3:00 PM - 4:00 PM', '3:00 PM - 4:00 PM'),
    ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM'),
    ('5:00 PM - 6:00 PM', '5:00 PM - 6:00 PM'),
)

BOOKING_TYPE = (
    ('create', 'create'),
    ('update', 'update'),
)
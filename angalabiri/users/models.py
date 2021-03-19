import random
import os
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    OneToOneField,
    Q,
    SlugField,
    CASCADE,
    SET_NULL,
    URLField,
    IPAddressField,
    GenericIPAddressField,
)
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone

from category.models import Category, Tag
from .validators import validate_user_photo_extension

MALE = "male"
FEMALE = "female"
OTHER = "other"
NOT_KNOWN = "Not Known"

GENDER = (
    ("", "Gender"),
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
    (NOT_KNOWN, "Not Known"),
)

NONE = "None"
MR = "Mr"
MRS = "Mrs"
MSS = "Mss"
DR = "Dr"
SIR = "Sir"
ENGR = "Engr"
MADAM = "Madam"

TITLE = (
    ("", "Prefix"),
    (MR, "Mr"),
    (MRS, "Mrs"),
    (MSS, "Mss"),
    (DR, "Dr"),
    (ENGR, "Engr"),
    (SIR, "Sir"),
    (MADAM, "Madam"),
)

QUEEN = "Queen"
KING = "King"
CHIEF = "Chief"
PRINCE = "Prince"
PRINCESS = "Princess"

ROYALTY = (
    ("", "Royal Status"),
    (QUEEN, "Queen"),
    (KING, "King"),
    (CHIEF, "Chief"),
    (PRINCE, "Prince"),
    (PRINCESS, "Princess"),
)

MASTERS = "PHD or Masters"
ALEVEL = "A-LEVEL"
SENIORHIGH = "Senior High"
JUNIORHIGH = "Junior High"
TERTIARY = "Tertiary"
PRIMARY = "Primary Level"
OTHER = "Other"

EDUCATIONAL_LEVEL = (
    ("", "Educational Level"),
    (MASTERS, "PHD or Masters"),
    (TERTIARY, "Tertiary/University/Polytechnic"),
    (ALEVEL, "A-Level"),
    (SENIORHIGH, "Senior High School"),
    (JUNIORHIGH, "Junior High School"),
    (PRIMARY, "Primary School"),
    (OTHER, "Other"),
)

BRASS = "Brass"
EKEREMOR = "Ekeremor"
KOLOKUMA = "Kolokuma Opokuma"
NEMBE = "Nembe"
OGBIA = "Ogbia"
SAGBAMA = "Sagbama"
SOUTHERN_IJAW = "Southern Ijaw"
YENAGOA = "Yenagoa"

BAYELSA_LGA = (
    ("", "LGA"),
    (BRASS, "Brass"),
    (EKEREMOR, "Ekeremor"),
    (KOLOKUMA, "Kolokuma Opokuma"),
    (NEMBE, "Nembe"),
    (OGBIA, "Ogbia"),
    (SAGBAMA, "Sagbama"),
    (SOUTHERN_IJAW, "Southern Ijaw"),
    (YENAGOA, "Yenagoa"),
)

CHAR_REGEX = "^[a-zA-Z]*$"
NUM_REGEX = "^[0-9]*$"
ZIP_REGEX = "^(^[0-9]{5}(?:[-\s]?[0-9]{4})$)"
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NIG_SIM = "/^+234[0-9]{11}/"


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def citizen_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "citizen/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


class User(AbstractUser):
    """Default user for angalabiri."""

    #: First and last name do not cover name patterns around the globe
    mid_name = CharField(
        _("Middle Name"),
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=CHAR_REGEX,
                message="Middle Name must be Alphabetic",
                code="invalid_input, only strings",
            )
        ],
    )
    first_name = CharField(
        _("First Name"),
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=CHAR_REGEX,
                message="First Name must be Alphabetic",
                code="invalid_input, only strings",
            )
        ],
    )
    last_name = CharField(
        _("Last Name"),
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=CHAR_REGEX,
                message="Last Name must be Alphabetic",
                code="invalid_input, only strings",
            )
        ],
    )
    dob = DateField(_("Date of Birth"), blank=True, null=True)
    photo = FileField(
        _("Profile Photo"),
        upload_to=citizen_image,
        validators=[validate_user_photo_extension],
        null=True,
        blank=True,
        help_text="supported formats: [jpeg/png/svg]",
    )
    phone = CharField(
        _("Phone Number"),
        max_length=14,
        validators=[
            RegexValidator(
                regex=NIG_SIM,
                message="Invalid Number",
                code="invalid_input, only 14 fields including +234xxxxxxxxxx",
            )
        ],
        help_text="Format: +234xxxxxxxxxx",
        unique=True,
        null=True,
        blank=True,
    )
    gender = CharField(_("Gender"), max_length=9, choices=GENDER, null=True, blank=True)
    status = CharField(
        _("Prefix"), max_length=8, choices=TITLE, null=True, blank=True
    )
    royals = CharField(
        _("Royal Status"), max_length=12, choices=ROYALTY, null=True, blank=True
    )
    lga = CharField(
        _("Local Government Area"),
        max_length=16,
        choices=BAYELSA_LGA,
        null=True,
        blank=True,
    )
    bvn = CharField(
        _("Bank Verification Number"),
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Invalid BVN",
                code="invalid_input, only 11 fields",
            )
        ],
        max_length=11,
        unique=True,
        null=True,
        blank=False,
    )
    own_shop = BooleanField(default=False, null=True, blank=True)
    accept_terms = BooleanField(default=False, null=True, blank=True)
    accept_cookies = BooleanField(default=False, null=True, blank=True)
    ip_address = GenericIPAddressField(_("Current IP Address"), null=True, blank=True)
    accessed_with = CharField(
        _("System IP Accessed with"), max_length=255, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.mid_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

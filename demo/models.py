from django.db import models
from django.contrib.auth.models import User

class ID_Proof(models.Model):
    aadhar_card = models.ImageField(null=True,upload_to='documents/')
    election_card = models.ImageField(null=True,upload_to='documents/')
    pan_card = models.ImageField(null=True,upload_to='documents/')

class Name(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

class Contact_Number(models.Model):
    mobile1 = models.CharField(max_length=15, null=True)
    mobile2 = models.CharField(max_length=15, null=True)
    telephone1 = models.CharField(max_length=15, null=True)
    telephone2 = models.CharField(max_length=15, null=True)

    def __str__(self):
        if self.mobile1 is not '' and self.mobile1 is not None:
            return self.mobile1
        else:
            return "No Number given."

class Temporary_Address(models.Model):
    house_no = models.CharField(max_length=100, null=True)
    street_no = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    at_po = models.CharField(max_length=100, null=True)
    town = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    google_pin = models.CharField(max_length=100, null=True)

class Permanent_Address(models.Model):
    house_no = models.CharField(max_length=100, null=True)
    street_no = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    at_po = models.CharField(max_length=100, null=True)
    town = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    google_pin = models.CharField(max_length=100, null=True)

class Emergency_Contact(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    relation = models.CharField(max_length=100, null=True)
    contact_number = models.OneToOneField(Contact_Number, null=True)
    house_no = models.CharField(max_length=100, null=True)
    street_no = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    at_po = models.CharField(max_length=100, null=True)
    town = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    google_pin = models.CharField(max_length=100, null=True)

class General_Profile(models.Model):
    id_proof = models.OneToOneField(ID_Proof, null=True, on_delete=models.CASCADE)
    name = models.OneToOneField(Name, null=True, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    contact_number = models.OneToOneField(Contact_Number, null=True, on_delete=models.CASCADE)
    temporary_address = models.OneToOneField(Temporary_Address, null=True, on_delete=models.CASCADE)
    permanent_address = models.OneToOneField(Permanent_Address, null=True, on_delete=models.CASCADE)
    emergency_contact = models.OneToOneField(Emergency_Contact, null=True, on_delete=models.CASCADE)
    physical_disability = models.CharField(max_length=100, null=True)

### General Profile Ends ###

class PG_Degree(models.Model):
    specialization = models.CharField(max_length=200, null=True)
    year_of_passing = models.CharField(max_length=200, null=True)
    percentage = models.CharField(max_length=200, null=True)
    university_name = models.CharField(max_length=500, null=True)

class Bachelors(models.Model):
    specialization = models.CharField(max_length=200, null=True)
    year_of_passing = models.CharField(max_length=200, null=True)
    percentage = models.CharField(max_length=200, null=True)
    university_name = models.CharField(max_length=500, null=True)

class Intermediate(models.Model):
    year_of_passing = models.CharField(max_length=200, null=True)
    percentage = models.CharField(max_length=200, null=True)
    state_board = models.CharField(max_length=500, null=True)

class SSC(models.Model):
    year_of_passing = models.CharField(max_length=200, null=True)
    percentage = models.CharField(max_length=200, null=True)
    state_board = models.CharField(max_length=500, null=True)

class Below_SSC(models.Model):
    year_of_passing = models.CharField(max_length=200, null=True)
    percentage = models.CharField(max_length=200, null=True)
    state_board = models.CharField(max_length=500, null=True)


class Educational_Profile(models.Model):
    pg_degree = models.OneToOneField(PG_Degree, null=True, on_delete=models.CASCADE)
    bachelors = models.OneToOneField(Bachelors, null=True, on_delete=models.CASCADE)
    intermediate = models.OneToOneField(Intermediate, null=True, on_delete=models.CASCADE)
    ssc = models.OneToOneField(SSC, null=True, on_delete=models.CASCADE)
    below_ssc = models.OneToOneField(Below_SSC, null=True, on_delete=models.CASCADE)


### EDUCATIONAL PROFILE ENDS ###
class JobExperience(models.Model):
    from_year = models.CharField(max_length=100,null=True)
    to_year = models.CharField(max_length=100,null=True)
    organisation = models.CharField(max_length=300, null=True)
    total_years = models.IntegerField(null=True)
    salary = models.CharField(max_length=200, null=True)
    reason_left = models.CharField(max_length=1000, null=True)

class JobProfile(models.Model):
    job_experience = models.ManyToManyField(JobExperience, null=True)

#### JOB PROFILE ENDS ####
class Skill(models.Model):
    skill = models.CharField(max_length=500, null=True)

class Skills(models.Model):
    values = models.ManyToManyField(Skill, null=True)

class Passport(models.Model):
    front_page = models.ImageField(null=True)
    back_page = models.ImageField(null=True)

class Bank_Passbook(models.Model):
    front_page = models.ImageField(null=True)
    back_page = models.ImageField(null=True)

class Visa(models.Model):
    front_page = models.ImageField(null=True)
    back_page = models.ImageField(null=True)

class Uploads(models.Model):
    passport = models.OneToOneField(Passport, null=True, on_delete=models.CASCADE)
    bank_passbook = models.OneToOneField(Bank_Passbook, null=True, on_delete=models.CASCADE)
    pg_degree = models.ImageField(null=True)
    bachelors = models.ImageField(null=True)
    intermediate = models.ImageField(null=True)
    ssc = models.ImageField(null=True)
    below_ssc = models.ImageField(null=True)
    visa = models.OneToOneField(Visa, null=True, on_delete=models.CASCADE)
    signature = models.ImageField(null=True)
    thumb_impression = models.ImageField(null=True)
    passport_size = models.ImageField(null=True)
    full_body = models.ImageField(null=True)
    medical = models.ImageField(null=True)
    video = models.FileField(null=True)

class Other_Details(models.Model):
    medical_issue = models.CharField(max_length=1000, null=True)
    current_salary = models.CharField(max_length=200, null=True)
    expected_salary = models.CharField(max_length=200, null=True)

class Maid(models.Model):
    general_profile = models.OneToOneField(General_Profile, null=True, on_delete=models.CASCADE)
    educational_profile = models.OneToOneField(Educational_Profile, null=True, on_delete=models.CASCADE)
    job_profile = models.OneToOneField(JobProfile, null=True, on_delete=models.CASCADE)
    uploads = models.OneToOneField(Uploads, null=True, on_delete=models.CASCADE)
    skills = models.OneToOneField(Skills, null=True, on_delete=models.CASCADE)
    other_details = models.OneToOneField(Other_Details, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=None, default=1)

    def __str__(self):
        name = self.general_profile.name
        if name is not None:
            return name.first_name + " " + name.last_name
        else:
            return self.id



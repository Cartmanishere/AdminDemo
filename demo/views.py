from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy,reverse
import datetime
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

def index(request):
    return render(request, 'demo/layout.html', {})

def login_user(request):
    if request.user.is_authenticated():
        return redirect("/")
    else:
        if request.method == "GET":
            return render(request, 'demo/sign_in.html', {})

        else:
            email = request.POST['email']
            password = request.POST['password']
            u = authenticate(username=email, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return redirect("/")

                else:
                    messages.add_message(request, messages.ERROR, "Your account has been disabled!")
                    return redirect('/')

            else:
                messages.add_message(request, messages.ERROR, "Invalid Password/Username.")
                return redirect('/login/')

@login_required(login_url='/login/')
def add_maid(request):
    if request.method == "GET":
        return render(request, 'demo/add_maid.html', {})

    #The clusterfuck begins
    if request.method == "POST":
        #name_fields
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        middle_name = request.POST.get('middle_name', None)
        # TODO:: Add validation if possible
        name = Name(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )
        name.save()
        #age
        age = request.POST.get('age', None)
        #telephone number
        mobile1 = request.POST.get('mobile1', None)
        mobile2 = request.POST.get('mobile2', None)
        telephone1 = request.POST.get('telephone1', None)
        telephone2 = request.POST.get('telephone2', None)
        contact_number = Contact_Number(
            mobile1=str(mobile1),
            mobile2=str(mobile2),
            telephone1=str(telephone1),
            telephone2=str(telephone2)
        )
        contact_number.save()
        house_no = request.POST.get('t_house_no', None)
        street_no = request.POST.get('t_street_no', None)
        area = request.POST.get('t_area', None)
        landmark = request.POST.get('t_landmark', None)
        at_po = request.POST.get('t_at_po', None)
        town = request.POST.get('t_town', None)
        district = request.POST.get('t_district', None)
        state = request.POST.get('t_state', None)
        country = request.POST.get('t_country', None)
        temporary_address = Temporary_Address(
            house_no=house_no,
            street_no=street_no,
            area=area,
            landmark=landmark,
            at_po=at_po,
            town=town,
            district=district,
            state=state,
            country=country
        )
        temporary_address.save()
        house_no = request.POST.get('p_house_no', None)
        street_no = request.POST.get('p_street_no', None)
        area = request.POST.get('p_area', None)
        landmark = request.POST.get('p_landmark', None)
        at_po = request.POST.get('p_at_po', None)
        town = request.POST.get('p_town', None)
        district = request.POST.get('p_district', None)
        state = request.POST.get('p_state', None)
        country = request.POST.get('p_country', None)
        permanent_address = Permanent_Address(
            house_no=house_no,
            street_no=street_no,
            area=area,
            landmark=landmark,
            at_po=at_po,
            town=town,
            district=district,
            state=state,
            country=country
        )
        permanent_address.save()
        first_name = request.POST.get('e_first_name', None)
        last_name = request.POST.get('e_last_name', None)
        middle_name = request.POST.get('e_middle_name', None)
        relation = request.POST.get('e_rel', None)
        mobile1 = request.POST.get('e_mobile1', None)
        mobile2 = request.POST.get('e_mobile2', None)
        telephone1 = request.POST.get('e_telephone1', None)
        telephone2 = request.POST.get('e_telephone2', None)
        house_no = request.POST.get('e_house_no', None)
        street_no = request.POST.get('e_street_no', None)
        area = request.POST.get('e_area', None)
        landmark = request.POST.get('e_landmark', None)
        at_po = request.POST.get('e_at_po', None)
        town = request.POST.get('e_town', None)
        district = request.POST.get('e_district', None)
        state = request.POST.get('e_state', None)
        country = request.POST.get('e_country', None)
        contact_number1 = Contact_Number(
            mobile1=str(mobile1),
            mobile2=str(mobile2),
            telephone1=str(telephone1),
            telephone2=str(telephone2)
        )
        contact_number1.save()
        emergency_contact = Emergency_Contact(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            relation=relation,
            contact_number=contact_number1,
            house_no=house_no,
            street_no=street_no,
            area=area,
            landmark=landmark,
            at_po=at_po,
            town=town,
            district=district,
            state=state,
            country=country
        )
        emergency_contact.save()
        aadhar_card = request.FILES.get('aadhar_card', None)
        election_card = request.FILES.get('election_card', None)
        pan_card = request.FILES.get('pan_card', None)
        id_proof = ID_Proof(
            aadhar_card=aadhar_card,
            election_card=election_card,
            pan_card=pan_card
        )
        id_proof.save()
        physical_disability = request.POST.get('physical_disability', None)
        general_profile = General_Profile(
            name=name,
            id_proof=id_proof,
            age=age,
            contact_number=contact_number,
            temporary_address=temporary_address,
            permanent_address=permanent_address,
            emergency_contact=emergency_contact,
            physical_disability=physical_disability
        )
        general_profile.save()
        specialization = request.POST.get('pg_specialization', None)
        year_of_passing = request.POST.get('pg_year_of_passing', None)
        percentage = request.POST.get('pg_percentage', None)
        university_name = request.POST.get('pg_university_name', None)
        pg_degree = PG_Degree(
            specialization=specialization,
            year_of_passsing=year_of_passing,
            percentage=percentage,
            university_name=university_name
        )
        pg_degree.save()
        specialization = request.POST.get('b_specialization', None)
        year_of_passing = request.POST.get('b_year_of_passing', None)
        percentage = request.POST.get('b_percentage', None)
        university_name = request.POST.get('b_university_name', None)
        bachelors = Bachelors(
            specialization=specialization,
            year_of_passsing=year_of_passing,
            percentage=percentage,
            university_name=university_name
        )
        bachelors.save()
        year_of_passing = request.POST.get('i_year_of_passing', None)
        percentage = request.POST.get('i_percentage', None)
        state_board = request.POST.get('i_state_board', None)
        intermediate = Intermediate(
            year_of_passsing=year_of_passing,
            percentage=percentage,
            state_board=state_board
        )
        intermediate.save()
        year_of_passing = request.POST.get('s_year_of_passing', None)
        percentage = request.POST.get('s_percentage', None)
        state_board = request.POST.get('s_state_board', None)
        ssc = SSC(
            year_of_passsing=year_of_passing,
            percentage=percentage,
            state_board=state_board
        )
        ssc.save()
        year_of_passing = request.POST.get('below_ssc_year_of_passing', None)
        percentage = request.POST.get('below_ssc_percentage', None)
        state_board = request.POST.get('below_ssc_state_board', None)
        below_ssc = Below_SSC(
            year_of_passsing=year_of_passing,
            percentage=percentage,
            state_board=state_board
        )
        below_ssc.save()
        educational_profile = Educational_Profile(
            pg_degree=pg_degree,
            bachelors=bachelors,
            intermediate=intermediate,
            ssc=ssc,
            below_ssc=below_ssc
        )
        educational_profile.save()

        job_profile = JobProfile()
        job_profile.save()
        job_experience = JobExperience(
            from_year=request.POST.get('1_from_year', None),
            to_year=request.POST.get('1_to_year', None),
            organisation=request.POST.get('1_organisation', None),
            salary=request.POST.get('1_salary', None),
            reason_left=request.POST.get('1_reason_left', None)
        )
        job_experience.save()
        job_profile.job_experience.add(job_experience)
        job_experience = JobExperience(
            from_year=request.POST.get('2_from_year', None),
            to_year=request.POST.get('2_to_year', None),
            organisation=request.POST.get('2_organisation', None),
            salary=request.POST.get('2_salary', None),
            reason_left=request.POST.get('2_reason_left', None)
        )
        job_experience.save()
        job_profile.job_experience.add(job_experience)
        job_profile.save()

        skills_list = request.POST.getlist('skills', [])
        skills_str = ""
        for i in skills_list:
            skills_str = skills_str + "|" + i

        skills = Skills(values=skills_str)
        skills.save()
        medical_issues = request.POST.get('medical_issues', None)
        current_salary = request.POST.get('current_salary', None)
        expected_salary = request.POST.get('expected_salary', None)
        other_details = Other_Details(
            medical_issue=medical_issues,
            current_salary=current_salary,
            expected_salary=expected_salary
        )
        other_details.save()

        passport = Passport(
            front_page=request.FILES.get('p_front_page', None),
            back_page= request.FILES.get('p_back_page', None)
        )
        passport.save()
        bank_passbook = Bank_Passbook(
            front_page=request.FILES.get('b_front_page', None),
            back_page=request.FILES.get('b_back_page', None)
        )
        bank_passbook.save()
        visa = Visa(
            front_page=request.FILES.get('v_front_page', None),
            back_page=request.FILES.get('v_back_page', None)
        )
        visa.save()
        uploads = Uploads(
            passport=passport,
            bank_passbook=bank_passbook,
            visa=visa,
            pg_degree=request.FILES.get('pg_degree_c', None),
            bachelors=request.FILES.get('b_certificate', None),
            intermediate=request.FILES.get('hsc', None),
            ssc=request.FILES.get('ssc', None),
            below_ssc=request.FILES.get('below_ssc', None),
            signature=request.FILES.get('signature', None),
            thumb_impression=request.FILES.get('thumb', None),
            passport_size=request.FILES.get('passport_size', None),
            full_body=request.FILES.get('full_size', None),
            medical=request.FILES.get('medical', None)
        )
        uploads.save()
        maid = Maid(
            general_profile=general_profile,
            educational_profile=educational_profile,
            job_profile=job_profile,
            skills=skills,
            other_details=other_details,
            uploads=uploads
        )
        maid.save()

        messages.success(request, "I will kill myself if this doesn't work soon.")
        return redirect('/')




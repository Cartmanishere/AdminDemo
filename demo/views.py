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

def is_agent(user):
    return user.groups.filter(name='Agent').exists()

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser


def add_profile(request, u, type=None):
    # name_fields
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
    # age
    age = request.POST.get('age', None)
    date_of_birth = request.POST.get('date_of_birth', None)
    # telephone number
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

    aadhar_card = request.FILES.get('aadhar_card', None)
    election_card = request.FILES.get('election_card', None)
    pan_card = request.FILES.get('pan_card', None)
    id_proof = ID_Proof(
        aadhar_card=aadhar_card,
        election_card=election_card,
        pan_card=pan_card
    )
    id_proof.save()
    if type =="admin":
        passport_size = request.FILES.get('passport_size', None)
        AdminProfile(
            user=u,
            id_proof=id_proof,
            name=name,
            age=age,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            temporary_address=temporary_address,
            permanent_address=permanent_address,
            passport_size=passport_size
        ).save()

    elif type=="agent":
        passport_size = request.FILES.get('passport_size', None)
        AgentProfile(
            user=u,
            id_proof=id_proof,
            name=name,
            age=age,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            temporary_address=temporary_address,
            permanent_address=permanent_address,
            passport_size=passport_size
        ).save()

    else:
        CustomerProfile(
            user=u,
            id_proof=id_proof,
            name=name,
            age=age,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            temporary_address=temporary_address,
            permanent_address=permanent_address,
        ).save()

def maid_delete(m):
    try:
        name = m.general_profile.name
        id_proof = m.general_profile.id_proof
        contact_number = m.general_profile.contact_number
        temporary_address = m.general_profile.temporary_address
        permanent_address = m.general_profile.permanent_address
        emergency_contact = m.general_profile.emergency_contact

        pg_degree = m.educational_profile.pg_degree
        bachelors = m.educational_profile.bachelors
        ssc = m.educational_profile.ssc
        intermediate = m.educational_profile.intermediate
        below_ssc = m.educational_profile.below_ssc

        job_profile = m.job_profile
        other_details = m.other_details
        skills = m.skills

        passport = m.uploads.passport
        visa = m.uploads.visa
        bank_passbook = m.uploads.bank_passbook

        name.delete()
        id_proof.delete()
        contact_number.delete()
        temporary_address.delete()
        permanent_address.delete()
        emergency_contact.delete()

        pg_degree.delete()
        bachelors.delete()
        ssc.delete()
        intermediate.delete()
        below_ssc.delete()

        job_profile.job_experience.all().delete()
        job_profile.delete()

        skills.skill.all().delete()
        skills.delete()

        passport.delete()
        bank_passbook.delete()
        visa.delete()

        other_details.delete()

        return True

    except Exception as e:
        print(e)
        return False

def index(request):
    maids = Maid.objects.all()
    if request.user.is_authenticated:
        request.user.is_agent = is_agent(request.user)
        request.user.is_admin = is_admin(request.user)
        request.user.is_customer = is_customer(request.user)

    return render(request, 'demo/maid_index.html', {'maids':maids})

@login_required(login_url='/login/')
def agent_index(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)

    if request.user.is_admin or request.user.is_superuser:
        u = User.objects.filter(groups__name="Agent")
        for i in u:
            i.no_of_maids = Maid.objects.filter(user=i).count()

        agents = list(u)
        agents.sort(key=lambda x: x.no_of_maids, reverse=True)
        return render(request, 'demo/admin/agent_index.html', {'agents': agents})
    else:
        messages.error(request, "You do not have permission to view this information.")
        return redirect('/')


@login_required(login_url='/login/')
def request_index(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)

    if request.user.is_admin or request.user.is_superuser:
        requests = Request.objects.all()

        return render(request, 'demo/request_index.html', {'requests': requests})

    elif request.user.is_customer:
        requests = Request.objects.filter(customer=request.user)
        return render(request, 'demo/request_index.html', {'requests': requests})

    elif request.user.is_agent:
        maids = Maid.objects.filter(user=request.user)
        requests =[]
        for i in maids:
            requests += list(Request.objects.filter(maid=i))

        return render(request, 'demo/request_index.html', {'requests': requests})


@login_required(login_url='/login/')
def request_add(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    if request.user.is_customer:
        id = request.POST.get('id')
        if id=="" or id==None:
            messages.error(request, "There was some error. Please try again.")
            return redirect('/')

        try:
            m = Maid.objects.get(id=int(id))
        except Exception:
            messages.error(request, "Maid does not exist.")
            return redirect('/')

        r = Request(
            customer=request.user,
            maid=m,
            payment_option=request.POST.get('payment_option'),
            status="Pending"
        ).save()

        messages.success(request, "Successfully requested quote. You can view this in requests section in the side menu.")
        return redirect('/')

    else:
        messages.error(request, "You cannot request a quote.")
        return redirect('/')

@login_required(login_url='/login/')
def customer_index(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    if request.user.is_admin or request.user.is_superuser:
        u = User.objects.filter(groups__name="Customer")
        return render(request, 'demo/admin/customer_index.html', {'customers': u})
    else:
        messages.error(request, "You do not have permission to view this information.")
        return redirect('/')


def signup_agent(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == "GET":
            return render(request, 'demo/agent/agent_sign_up.html', {})

        else:
            email = request.POST['email']
            password = request.POST['password']
            group = Group.objects.get(name="Agent")
            u = User(username=email, password=password)
            u.set_password(password)
            u.save()
            u.groups.add(group)

            add_profile(request, u, type="agent")

            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, "Thank you for signing up!")

            return redirect('/')


def signup_admin(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == "GET":
            return render(request, 'demo/admin/admin_sign_up.html', {})

        else:
            email = request.POST['email']
            password = request.POST['password']
            group = Group.objects.get(name="Admin")
            u = User(username=email, password=password)
            u.set_password(password)
            u.save()
            u.groups.add(group)

            add_profile(request, u, type="admin")


            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, "Thank you for signing up!")

            return redirect('/')

def signup_customer(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == "GET":
            return render(request, 'demo/customer/customer_sign_up.html', {})

        else:
            email = request.POST['email']
            password = request.POST['password']
            group = Group.objects.get(name="Customer")
            u = User(username=email, password=password)
            u.set_password(password)
            u.save()
            u.groups.add(group)

            add_profile(request, u, type="customer")


            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, "Thank you for signing up!")

            return redirect('/')

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
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    if request.method == "GET":
        if is_admin(request.user) or is_agent(request.user):
            return render(request, 'demo/agent/add_maid.html', {})
        else:
            messages.error(request, "You cannot add a maid.")
            return redirect('/')

    #The clusterfuck begins
    if request.method == "POST":
        if is_admin(request.user) or is_agent(request.user):
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
                year_of_passing=year_of_passing,
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
                year_of_passing=year_of_passing,
                percentage=percentage,
                university_name=university_name
            )
            bachelors.save()
            year_of_passing = request.POST.get('i_year_of_passing', None)
            percentage = request.POST.get('i_percentage', None)
            state_board = request.POST.get('i_state_board', None)
            intermediate = Intermediate(
                year_of_passing=year_of_passing,
                percentage=percentage,
                state_board=state_board
            )
            intermediate.save()
            year_of_passing = request.POST.get('s_year_of_passing', None)
            percentage = request.POST.get('s_percentage', None)
            state_board = request.POST.get('s_state_board', None)
            ssc = SSC(
                year_of_passing=year_of_passing,
                percentage=percentage,
                state_board=state_board
            )
            ssc.save()
            year_of_passing = request.POST.get('below_ssc_year_of_passing', None)
            percentage = request.POST.get('below_ssc_percentage', None)
            state_board = request.POST.get('below_ssc_state_board', None)
            below_ssc = Below_SSC(
                year_of_passing=year_of_passing,
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
            skills = Skills()
            skills.save()
            skills_list = request.POST.getlist('skills', [])
            for i in skills_list:
                skill = Skill(skill=i)
                skill.save()
                skills.values.add(skill)

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
                uploads=uploads,
                user=request.user
            )
            maid.save()

            messages.success(request, "Maid has been created.")
            return redirect('/')
        else:
            messages.error(request, "You cannot add a maid.")
            return redirect('/')


def view_maid(request, id):
    if request.user.is_authenticated:
        request.user.is_agent = is_agent(request.user)
        request.user.is_agent = is_agent(request.user)
        request.user.is_admin = is_admin(request.user)
        request.user.is_customer = is_customer(request.user)
    try:
        maid = Maid.objects.get(id=id)
        maid.general_profile.id_proof.aadhar_card.is_there = bool(maid.general_profile.id_proof.aadhar_card)
        maid.general_profile.id_proof.election_card.is_there = bool(maid.general_profile.id_proof.election_card)
        maid.general_profile.id_proof.pan_card.is_there = bool(maid.general_profile.id_proof.pan_card)
        maid.uploads.passport.front_page.is_there = bool(maid.uploads.passport.front_page)
        maid.uploads.passport.back_page.is_there = bool(maid.uploads.passport.back_page)
        maid.uploads.bank_passbook.front_page.is_there = bool(maid.uploads.bank_passbook.front_page)
        maid.uploads.bank_passbook.back_page.is_there = bool(maid.uploads.bank_passbook.back_page)
        maid.uploads.visa.front_page.is_there = bool(maid.uploads.visa.front_page)
        maid.uploads.visa.back_page.is_there = bool(maid.uploads.visa.back_page)
        maid.uploads.pg_degree.is_there = bool(maid.uploads.pg_degree)
        maid.uploads.bachelors.is_there = bool(maid.uploads.bachelors)
        maid.uploads.intermediate.is_there = bool(maid.uploads.intermediate)
        maid.uploads.ssc.is_there = bool(maid.uploads.ssc)
        maid.uploads.below_ssc.is_there = bool(maid.uploads.below_ssc)
        maid.uploads.signature.is_there = bool(maid.uploads.signature)
        maid.uploads.thumb_impression.is_there = bool(maid.uploads.thumb_impression)
        maid.uploads.passport_size.is_there = bool(maid.uploads.passport_size)
        maid.uploads.medical.is_there = bool(maid.uploads.medical)
        maid.uploads.full_body.is_there = bool(maid.uploads.full_body)

    except Exception as e:
        messages.error(request, "This maid does not exist.")
        return redirect('/')

    return render(request, 'demo/view_maid.html', {'maid': maid})


@login_required(login_url='/login/')
def delete_maid(request, id):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    try:
        m = Maid.objects.get(id=id)
    except Exception as e:
        print(e)
        messages.error(request, "No such maid exists.")
        return redirect('/')

    if (is_agent(request.user) and m.user==request.user) or is_admin(request.user):
        maid_delete(m)
        messages.success(request, "Maid information has been deleted.")
        return redirect('/')

    else:
        messages.error(request, "You do not have permission to delete this maid.")
        return redirect('/')

@login_required(login_url='/login/')
def admin_profile(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    if is_admin(request.user):
        admin_profile = AdminProfile.objects.get(user=request.user)
        admin_profile.id_proof.aadhar_card.is_there = bool(admin_profile.id_proof.aadhar_card)
        admin_profile.id_proof.election_card.is_there = bool(admin_profile.id_proof.election_card)
        admin_profile.id_proof.pan_card.is_there = bool(admin_profile.id_proof.pan_card)
        admin_profile.passport_size = bool(admin_profile.passport_size)
        return render(request, 'demo/agent/agent_profile.html', {'profile':admin_profile})


    else:
        messages.error(request, "You are not admin.")
        return redirect('/')

@login_required(login_url='/login/')
def agent_profile(request, id=None):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)

    if is_agent(request.user):
        agent_profile = AgentProfile.objects.get(user=request.user)
        agent_profile.id_proof.aadhar_card.is_there = bool(agent_profile.id_proof.aadhar_card)
        agent_profile.id_proof.election_card.is_there = bool(agent_profile.id_proof.election_card)
        agent_profile.id_proof.pan_card.is_there = bool(agent_profile.id_proof.pan_card)
        agent_profile.passport_size = bool(agent_profile.passport_size)
        return render(request, 'demo/agent/agent_profile.html', {'profile': agent_profile})

    elif is_admin(request.user):
        if id is not None:
            try:
                u = User.objects.get(id=id)
            except Exception as e:
                messages.error(request, "Agent does not exist.")
                return redirect('/')

            agent_profile = AgentProfile.objects.get(user=u)
            agent_profile.id_proof.aadhar_card.is_there = bool(agent_profile.id_proof.aadhar_card)
            agent_profile.id_proof.election_card.is_there = bool(agent_profile.id_proof.election_card)
            agent_profile.id_proof.pan_card.is_there = bool(agent_profile.id_proof.pan_card)
            agent_profile.passport_size = bool(agent_profile.passport_size)
            return render(request, 'demo/agent/agent_profile.html', {'profile': agent_profile})

        else:
            messages.error(request, "No agent found.")
            return redirect('/')

    else:
        messages.error(request, 'You do not have permission for this.')
        return redirect('/')

@login_required(login_url='/login/')
def customer_profile(request, id=None):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)

    if is_agent(request.user):
        customer_profile = CustomerProfile.objects.get(user=request.user)
        customer_profile.id_proof.aadhar_card.is_there = bool(customer_profile.id_proof.aadhar_card)
        customer_profile.id_proof.election_card.is_there = bool(customer_profile.id_proof.election_card)
        customer_profile.id_proof.pan_card.is_there = bool(customer_profile.id_proof.pan_card)
        return render(request, 'demo/agent/customer_profile.html', {'profile': customer_profile})

    elif is_admin(request.user):
        if id is not None:
            try:
                u = User.objects.get(id=id)
            except Exception as e:
                messages.error(request, "Customer does not exist.")
                return redirect('/')

            customer_profile = CustomerProfile.objects.get(user=u)
            customer_profile.id_proof.aadhar_card.is_there = bool(customer_profile.id_proof.aadhar_card)
            customer_profile.id_proof.election_card.is_there = bool(customer_profile.id_proof.election_card)
            customer_profile.id_proof.pan_card.is_there = bool(customer_profile.id_proof.pan_card)
            return render(request, 'demo/agent/agent_profile.html', {'profile': customer_profile})

        else:
            messages.error(request, "No agent found.")
            return redirect('/')

    else:
        messages.error(request, 'You do not have permission for this.')
        return redirect('/')

@login_required(login_url='/login/')
def delete_agent(request, id):
    if request.user.is_superuser or is_admin(request.user):
        try:
            u = User.objects.get(id=id)
        except Exception as e:
            messages.error(request, "This user does not exist")
            return redirect('/')

        profile = AgentProfile.objects.get(user=u)
        name = profile.name
        id_proof = profile.id_proof
        contact_number = profile.contact_number
        temporary_address = profile.temporary_address
        permanent_address = profile.permanent_address
        m = Maid.objects.filter(user=u)
        for i in m:
            i.user = None
            i.save()

        name.delete()
        id_proof.delete()
        contact_number.delete()
        temporary_address.delete()
        permanent_address.delete()
        u.delete()
        profile.delete()
        messages.success(request, "Successfully deleted agent.")
        return redirect('/')

    else:
        messages.error(request, "You have do not permission to do this operation.")
        return redirect('/')


@login_required(login_url='/login/')
def delete_customer(request, id):
    if request.user.is_superuser or is_admin(request.user):
        try:
            u = User.objects.get(id=id)
        except Exception as e:
            messages.error(request, "This user does not exist")
            return redirect('/')

        profile = CustomerProfile.objects.get(user=u)
        name = profile.name
        id_proof = profile.id_proof
        contact_number = profile.contact_number
        temporary_address = profile.temporary_address
        permanent_address = profile.permanent_address
        ## Delete Reuqests

        name.delete()
        id_proof.delete()
        contact_number.delete()
        temporary_address.delete()
        permanent_address.delete()
        u.delete()
        profile.delete()
        messages.success(request, "Successfully deleted customer.")
        return redirect('/')

    else:
        messages.error(request, "You have do not permission to do this operation.")
        return redirect('/')


@login_required(login_url='/login/')
def delete_request(request, id):
    try:
        u = Request.objects.get(id=id)
    except Exception as e:
        messages.error(request, "This request does not exist")
        return redirect('/')

    if request.user.is_superuser or is_admin(request.user) or u.customer==request.user:
        u.delete()

        messages.success(request, "Successfully deleted request.")
        return redirect('/')

    else:
        messages.error(request, "You have do not permission to do this operation.")
        return redirect('/')

@login_required(login_url='/login/')
def status_change(request):
    request.user.is_agent = is_agent(request.user)
    request.user.is_admin = is_admin(request.user)
    request.user.is_customer = is_customer(request.user)
    try:
        id = request.POST.get('id')
        print(id)
        r = Request.objects.get(id=int(id))

    except Exception as e:
        messages.error(request, "This request does not exist")
        print(e)
        return redirect('/')
    if request.user.is_agent:
        maids = Maid.objects.filter(user=request.user)
    else:
        maids = None

    if request.user.is_admin or request.user.is_superuser or (request.user.is_agent and r.maid in maids):
        status = request.POST.get('status')
        r.status = status
        r.save()
        messages.success(request, "Request status changed.")
        return redirect('/requests/')

    else:
        messages.error(request, "You do not have permission to do this operation.")
        return redirect('/')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

'''
This
project
has
been
an
harrowing
experience.
I
cannot
imagine
how
I
managed
it.
I 
am 
leaving
this
long
comment
talking
about
useless
things
because
I
want
to
make
this
file
have -
not 
more
or
less
but
exactly
1000
lines
'''
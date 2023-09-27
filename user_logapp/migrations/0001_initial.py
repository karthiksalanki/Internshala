# Generated by Django 4.2.2 on 2023-09-23 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500)),
                ('Location', models.CharField(blank=True, max_length=500, null=True)),
                ('CompanyLogo', models.ImageField(upload_to='Company/')),
                ('Industry', models.CharField(blank=True, max_length=500, null=True)),
                ('No_of_Emps', models.CharField(blank=True, max_length=250, null=True)),
                ('Hiring_since', models.DateField(auto_now_add=True)),
                ('Opportunities_posted', models.CharField(blank=True, max_length=250, null=True)),
                ('Candidates_hired', models.CharField(blank=True, max_length=250, null=True)),
                ('About', models.TextField()),
            ],
            options={
                'verbose_name': 'CompanyProfile',
                'verbose_name_plural': 'CompanyProfile',
            },
        ),
        migrations.CreateModel(
            name='Internships',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(max_length=500)),
                ('Company_name', models.CharField(max_length=500)),
                ('Location', models.CharField(max_length=500)),
                ('Work_mode', models.CharField(choices=[('wfm', 'work from home'), ('office', 'InOffice')], default='InOffice', max_length=250)),
                ('Skills', models.CharField(max_length=500)),
                ('Experience', models.CharField(max_length=250)),
                ('Salary', models.PositiveIntegerField(blank=True, null=True)),
                ('date_of_post', models.DateField(auto_now_add=True)),
                ('Responsibilities', models.TextField(blank=True, null=True)),
                ('Eligibility', models.TextField(blank=True, null=True)),
                ('Perks', models.TextField(blank=True, null=True)),
                ('No_of_openings', models.PositiveIntegerField(blank=True, null=True)),
                ('Count', models.PositiveIntegerField(default=0)),
                ('Duration', models.CharField(blank=True, max_length=250, null=True)),
                ('CompanyProfile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user_logapp.companyprofile')),
            ],
            options={
                'verbose_name': 'Internships',
                'verbose_name_plural': 'Internships',
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(max_length=500)),
                ('Company_name', models.CharField(max_length=500)),
                ('Location', models.CharField(max_length=500)),
                ('Work_mode', models.CharField(choices=[('wfm', 'work from home'), ('office', 'InOffice')], default='InOffice', max_length=250)),
                ('Skills', models.CharField(max_length=500)),
                ('Salary', models.PositiveIntegerField(blank=True, null=True)),
                ('date_of_post', models.DateField(auto_now_add=True)),
                ('Responsibilities', models.TextField(blank=True, null=True)),
                ('Eligibility', models.TextField(blank=True, null=True)),
                ('Perks', models.TextField(blank=True, null=True)),
                ('No_of_openings', models.PositiveIntegerField(blank=True, null=True)),
                ('Count', models.PositiveIntegerField(default=0)),
                ('Experience', models.CharField(max_length=250)),
                ('CompanyProfile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user_logapp.companyprofile')),
            ],
            options={
                'verbose_name': 'Jobs',
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='Savedapplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.internships')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.jobs')),
            ],
            options={
                'verbose_name': 'Postsave',
                'verbose_name_plural': 'Postsave',
            },
        ),
        migrations.CreateModel(
            name='myApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('internship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.internships')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.jobs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MyApplications',
                'verbose_name_plural': 'MyApplications',
            },
        ),
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('applicant_skills', models.CharField(blank=True, max_length=200, null=True)),
                ('relocation', models.CharField(blank=True, max_length=250, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='Resumes/jobs/')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.jobs')),
            ],
            options={
                'verbose_name': 'JobApplications',
                'verbose_name_plural': 'JobApplications',
            },
        ),
        migrations.CreateModel(
            name='InternApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('applicant_skills', models.CharField(blank=True, max_length=200, null=True)),
                ('relocation', models.CharField(blank=True, max_length=250, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='Resumes/internship/')),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_logapp.internships')),
            ],
            options={
                'verbose_name': 'InternshipApplications',
                'verbose_name_plural': 'InternshipApplications',
            },
        ),
    ]

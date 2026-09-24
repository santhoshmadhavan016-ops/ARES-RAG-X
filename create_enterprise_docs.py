from pathlib import Path


DOCUMENTS = {

    "work_from_home_policy.txt": """
NOVA CORP — WORK FROM HOME POLICY

Eligibility

Employees may work from home when their role supports remote work and their manager approves the request.

Working Hours

Employees working remotely must follow their normal working hours and remain available during core business hours.

Attendance

Employees must remain reachable through approved communication tools during working hours.

Security

Employees must use approved company devices and secure connections when accessing company systems remotely.

Meetings

Employees are expected to attend scheduled online meetings and maintain professional communication.

Performance

Remote employees are evaluated using the same performance standards as employees working from the office.
""",

    "employee_travel_policy.txt": """
NOVA CORP — EMPLOYEE TRAVEL POLICY

Travel Approval

Business travel must be approved by the employee's manager before any booking is made.

Flights

Employees should select reasonable economy-class flights for normal business travel.

Hotels

Hotel bookings must follow the company's approved travel budget.

Travel Expenses

Reasonable business travel expenses may be reimbursed when valid receipts are submitted.

International Travel

International business travel requires additional approval from the department head.

Travel Safety

Employees should follow company travel safety guidelines while travelling for business.
""",

    "expense_reimbursement_policy.txt": """
NOVA CORP — EXPENSE REIMBURSEMENT POLICY

Eligible Expenses

Employees may claim reasonable business expenses incurred while performing approved company activities.

Receipts

Employees must submit receipts for expenses that require supporting documentation.

Submission Deadline

Expense claims should normally be submitted within thirty days of the expense.

Approval

Expense reports must be reviewed and approved by the employee's manager.

Personal Expenses

Personal expenses are not eligible for reimbursement.

False Claims

Submitting false or misleading expense information may result in disciplinary action.
""",

    "performance_management_policy.txt": """
NOVA CORP — PERFORMANCE MANAGEMENT POLICY

Performance Reviews

Employees receive regular performance reviews based on their responsibilities and objectives.

Goals

Employees and managers should establish measurable performance goals.

Feedback

Managers should provide constructive feedback throughout the review period.

Performance Improvement

Employees who do not meet expected performance standards may receive a performance improvement plan.

Promotions

Promotion decisions consider performance, skills, responsibilities, and business requirements.

Development

Employees are encouraged to identify training and development opportunities.
""",

    "training_development_policy.txt": """
NOVA CORP — TRAINING AND DEVELOPMENT POLICY

Training Programs

Nova Corp provides training programs to improve employee skills and professional development.

Mandatory Training

Employees must complete training programs required for their role or department.

Technical Training

Employees may request technical training related to their responsibilities.

External Courses

External courses may require manager approval before registration.

Certifications

Employees may request support for professional certifications when relevant to their role.

Learning Time

Managers should provide reasonable opportunities for employees to participate in approved learning activities.
""",

    "code_of_conduct.txt": """
NOVA CORP — CODE OF CONDUCT

Professional Behavior

Employees must behave professionally and respectfully when interacting with colleagues, customers, and business partners.

Harassment

Harassment, discrimination, and inappropriate workplace behavior are not permitted.

Conflicts of Interest

Employees must disclose situations that may create a conflict between personal interests and company responsibilities.

Confidentiality

Employees must protect confidential company and customer information.

Company Property

Employees must use company property responsibly.

Reporting

Employees should report serious violations of the code of conduct through approved company channels.
""",

    "data_privacy_policy.txt": """
NOVA CORP — DATA PRIVACY POLICY

Personal Data

Employees must handle personal information according to company privacy requirements.

Data Collection

Personal data should only be collected for legitimate business purposes.

Data Access

Access to personal information must be limited to authorized employees.

Data Sharing

Personal information must not be shared with unauthorized individuals or organizations.

Data Retention

Personal information should be retained only for as long as required for legitimate business purposes.

Privacy Incidents

Suspected privacy incidents must be reported to the appropriate security or privacy team.
""",

    "customer_service_policy.txt": """
NOVA CORP — CUSTOMER SERVICE POLICY

Customer Communication

Employees must communicate with customers professionally and respectfully.

Response Time

Customer requests should be acknowledged within the service team's expected response time.

Escalation

Complex or unresolved customer issues should be escalated to the appropriate manager.

Customer Information

Customer information must be handled securely and confidentially.

Complaints

Customer complaints should be documented and handled according to the approved escalation process.

Service Quality

Employees should aim to provide accurate, consistent, and helpful service.
""",

    "remote_access_policy.txt": """
NOVA CORP — REMOTE ACCESS POLICY

Secure Connection

Employees accessing company systems remotely must use approved secure connections.

Authentication

Employees must use required authentication controls when accessing company resources remotely.

Public Networks

Sensitive company operations should not be performed using unsecured public networks.

Company Devices

Employees should use approved company devices for remote access.

Access Monitoring

Remote access activity may be monitored for security purposes.

Incident Reporting

Unauthorized remote access or suspicious activity must be reported immediately.
""",

    "software_development_policy.txt": """
NOVA CORP — SOFTWARE DEVELOPMENT POLICY

Code Review

Software changes should be reviewed by another authorized developer before production deployment.

Version Control

Source code must be stored in approved version control systems.

Testing

Developers should perform appropriate testing before releasing software.

Security

Applications must follow approved secure development practices.

Documentation

Important software components should have appropriate technical documentation.

Production Access

Production systems should only be accessed by authorized employees.
""",

    "database_access_policy.txt": """
NOVA CORP — DATABASE ACCESS POLICY

Access Control

Database access must be granted only to employees who require it for their responsibilities.

Authentication

Employees must use approved authentication methods when accessing company databases.

Sensitive Data

Sensitive database information must be protected from unauthorized access.

Access Reviews

Database permissions should be reviewed periodically.

Data Changes

Important production data changes should be authorized and logged.

Incident Reporting

Unauthorized database access must be reported to the security team immediately.
""",

    "acceptable_use_policy.txt": """
NOVA CORP — ACCEPTABLE USE POLICY

Company Systems

Company computers and systems should primarily be used for legitimate business activities.

Internet Usage

Employees must use internet access responsibly and must not access prohibited content using company systems.

Email

Company email should be used for professional communication.

Software

Employees must not install unauthorized applications on company devices.

Security

Employees must follow company security requirements when using technology resources.

Monitoring

Company systems may be monitored to protect business resources and information.
""",

    "employee_onboarding_policy.txt": """
NOVA CORP — EMPLOYEE ONBOARDING POLICY

Orientation

New employees must complete the company's onboarding process.

Documentation

Employees must provide required employment and identification documentation through approved channels.

System Access

Required system accounts should be created according to the employee's role.

Training

New employees must complete mandatory company and security training.

Manager Responsibilities

Managers should provide new employees with role expectations and necessary resources.

Probation

Employees may be subject to a probationary period according to their employment terms.
""",

    "employee_offboarding_policy.txt": """
NOVA CORP — EMPLOYEE OFFBOARDING POLICY

Notice Period

Employees leaving the company must follow the notice requirements in their employment agreement.

Company Property

Employees must return company laptops, access cards, and other company property.

System Access

Employee system access should be removed according to the approved offboarding process.

Data

Employees must not retain confidential company information after leaving the organization.

Knowledge Transfer

Employees may be required to transfer important responsibilities and documentation.

Final Clearance

The employee must complete the required clearance process before departure.
""",

    "meeting_policy.txt": """
NOVA CORP — MEETING POLICY

Meeting Preparation

Employees should review the purpose and agenda before attending important meetings.

Punctuality

Employees should join scheduled meetings on time.

Participation

Participants are expected to contribute appropriately to discussions.

Online Meetings

Employees attending online meetings should use reliable connections and professional communication.

Documentation

Important decisions and action items should be documented.

Meeting Efficiency

Meetings should be kept focused and limited to necessary participants.
""",

    "workplace_safety_policy.txt": """
NOVA CORP — WORKPLACE SAFETY POLICY

Safe Workplace

Employees must follow workplace safety instructions and report unsafe conditions.

Emergency Procedures

Employees must follow company emergency procedures during incidents.

Equipment

Company equipment should be used according to safety instructions.

Accidents

Workplace accidents must be reported to the appropriate manager immediately.

Emergency Exits

Employees must keep emergency exits clear and accessible.

Training

Employees must complete required workplace safety training.
""",

    "information_classification_policy.txt": """
NOVA CORP — INFORMATION CLASSIFICATION POLICY

Public Information

Information approved for public distribution may be shared externally.

Internal Information

Internal company information should only be shared with authorized employees.

Confidential Information

Confidential information must be protected from unauthorized access.

Restricted Information

Restricted information requires additional security controls and limited access.

Data Handling

Employees must store information using approved company systems.

Incident Reporting

Misclassified or accidentally exposed information must be reported to the appropriate security team.
""",

    "asset_management_policy.txt": """
NOVA CORP — ASSET MANAGEMENT POLICY

Company Assets

Company technology assets must be assigned to authorized employees.

Asset Records

Company assets should be recorded in the approved asset management system.

Asset Protection

Employees are responsible for protecting assigned company equipment.

Loss

Lost or stolen company equipment must be reported immediately.

Transfers

Company assets may only be transferred through the approved process.

Return

Employees must return assigned assets when requested or when leaving the company.
""",

    "communication_policy.txt": """
NOVA CORP — COMMUNICATION POLICY

Professional Communication

Employees must communicate respectfully across company communication channels.

Email

Business emails should be clear, professional, and appropriate for the intended audience.

Messaging

Company messaging tools should be used for legitimate business communication.

Confidential Information

Confidential information must not be shared through unauthorized communication channels.

External Communication

Employees should not represent the company publicly unless authorized.

Escalation

Important communication issues should be escalated to the appropriate manager.
"""
}


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

created = 0

for filename, content in DOCUMENTS.items():

    file_path = DOCUMENTS_DIR / filename

    file_path.write_text(
        content.strip(),
        encoding="utf-8"
    )

    print(f"Created: {filename}")

    created += 1


print("\n" + "=" * 60)
print(f"Created {created} enterprise documents.")
print("=" * 60)
print(f"Location: {DOCUMENTS_DIR}")
import random
import pandas as pd

job_categories = {
    "Software Engineer": [
        "Python  and object-oriented programming",
        "Java SpringBoot microservices",
        "Git branching and merging strategies",
        "SQL query optimization for PostgreSQL",
        "RESTfulAPI design and documentation",
        "Docker Compose for multi-container apps",
        "Continuous Integration with Jenkins",
        "Unit testing with pytest",
        "Linux shell scripting for automation",
        "Agile Scrum team collaboration",
        "Frontend development with React.js",
        "Cloud deployment on AWS ",
        "Code review and static analysis tools",
        "Debugging with VSCode and GDB",
        "Performance profiling and memory management"
    ],
    "Data Scientist": [
        "Supervised and unsupervised machinelearning",
        "Feature engineering for tabular data",
        "Data cleaning with Pandas",
        "Statistical hypothesis testing",
        "Deeplearning with TensorFlow and Keras",
        "Model deployment with FastAPI",
        "Data visualization using Seaborn and Matplotlib",
        "Big data processing with Spark",
        "Natural Language Processing (NLP) techniques",
        "Hyperparameter tuning with GridSearchCV",
        "Time series forecasting with ARIMA",
        "Dimensionality reduction (PCA, t-SNE)",
        "SQL for data extraction and transformation",
        "Experiment tracking with MLflow",
        "Business analytics and KPI reporting"
    ],
    "Digital Marketing Specialist": [
        "SEO keyword research and on-page optimization",
        "Google Ads campaign setup and A/B testing",
        "Facebook Ads audience targeting",
        "Copywriting for landing pages and emails",
        "Email marketing automation with Mailchimp",
        "Conversion rate optimization (CRO)",
        "Content calendar planning and execution",
        "Social media analytics with Hootsuite",
        "Influencer outreach and partnership management",
        "Video marketing for YouTube and TikTok",
        "Retargeting strategies for e-commerce",
        "Google Analytics event tracking",
        "Competitor analysis and benchmarking",
        "Lead generation through LinkedIn",
        "Reporting and dashboard creation"
    ],
   
    "Cybersecurity Analyst": [
        "Network intrusion detection and prevention",
        "Vulnerability assessment and penetration testing",
        "Incident response and forensics",
        "Firewall configuration and management",
        "Security information and event management (SIEM)",
        "Encryption standards and protocols",
        "Risk analysis and mitigation",
        "Security awareness training",
        "Cloud security for AWS and Azure",
        "Identity and access management (IAM)",
        "Malware analysis and reverse engineering",
        "Compliance with GDPR and HIPAA",
        "Patch management and system hardening",
        "Threat intelligence gathering",
        "Security policy development"
    ],
    "Project Manager": [
        "Project planning and scheduling with MS Project",
        "Stakeholder communication and reporting",
        "Risk management and mitigation strategies",
        "Resource allocation and budgeting",
        "Agile and Waterfall methodologies",
        "Team leadership and conflict resolution",
        "Change management processes",
        "Quality assurance and control",
        "Vendor management and contract negotiation",
        "Performance tracking with KPIs",
        "Meeting facilitation and documentation",
        "Project closure and lessons learned",
        "Remote team coordination",
        "Scope management and requirements gathering",
        "Presentation to executive leadership"
    ]
}

templates = [
    "We are seeking a highly skilled {role} with extensive experience in {skills}. The ideal candidate will demonstrate leadership, adaptability, and a commitment to continuous improvement, contributing to innovative projects.",
    "Join our forward-thinking organization as a {role}. Candidates should possess advanced knowledge in {skills}, strong analytical abilities, and excellent communication skills to shape our strategies and deliver outstanding results.",
    "We have an exciting opportunity for a {role} who excels in {skills}. In this role, you will manage complex tasks, mentor colleagues, and ensure the highest standards of quality, essential for achieving our ambitious goals.",
    "Our company is searching for a dedicated {role} with proven proficiency in {skills}. You will be responsible for leading initiatives, optimizing processes, and fostering a culture of collaboration and innovation.",
    "As a {role}, you will leverage your experience in {skills} to solve challenging problems and drive impactful change. We value proactive, detail-oriented professionals passionate about making a difference.",
    "Become part of our dynamic team as a {role}. Your background in {skills} will enable you to contribute to strategic planning, process improvement, and the successful execution of key projects.",
    "We are looking for a {role} with a strong foundation in {skills}. You will work closely with stakeholders, develop effective solutions, and support the growth and development of our organization.",
    "Seeking an experienced {role} with expertise in {skills}. You will be involved in decision-making, project management, and the implementation of best practices to ensure our continued success."
]

def generate_fake_job_ads(n=100):
    ads = []
    for _ in range(n):
        role = random.choice(list(job_categories.keys()))
        selected_skills = ", ".join(random.sample(job_categories[role], k=random.randint(5, 9)))
        text = random.choice(templates).format(role=role, skills=selected_skills)
        ads.append({"title": role, "description": text})
    return pd.DataFrame(ads)

df = generate_fake_job_ads(30000)
df.to_csv("job_ads.csv", index=False, encoding="utf-8")
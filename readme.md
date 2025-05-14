# UWI Stats Platform


**Team:** PurpleStats  
*A web-based platform for the University of the West Indies to manage and publish statistical reports and visual data representations. Built for INFO2602.*


**Time spent:** ~3 weeks (Design, Development, Testing, Deployment)


---


## User Stories


### Required
- Admin and Regular User roles with login/signup functionality  
- Admins can upload reports (PDF) and charts (image + metadata)  
- Users can view and filter reports by year, campus, and type  
- Users can view and filter charts by title and type  
- Admins can edit chart titles and delete charts  


### Stretch
- Clean, responsive UI using MaterializeCSS  
- System deployed using Render  
- REST-based authentication for both Admin and Regular User apps  
- Report and chart data persist using SQLAlchemy  
- Ephemeral storage for uploaded files on Render cloud  


---


## Video Walkthrough
 [Click here to watch the full walkthrough](https://youtu.be/0nz8FD7I94A?si=VbAaFlx3sOHYykZu)


---


## Technologies Used


| Technology       | Purpose                                  |
|------------------|------------------------------------------|
| FlaskMVC         | Project template                         |
| Flask + SQLAlchemy | Backend logic and ORM                   |
| MaterializeCSS   | Frontend framework                       |
| Coolors          | Color palette selection                  |
| Render           | App deployment + ephemeral file storage  |
| GitHub           | Code version control                     |
| WebLabs          | Course support platform                  |


---


##  Live Site


-  [Deployed App](https://info2602statsapp-zfwk.onrender.com)  
-  [GitHub Repo](https://github.com/DenelleMohammed/INFO2602StatsApp)


---


##  Group Members


| Name              | Student ID | Role        | GitHub Username    |
|-------------------|------------|-------------|---------------------|
| De-Nisse Serrette | 816039244  | Marketing   | denisseee           |
| Denelle Mohammed  | 816039297  | DevOps      | DenelleMohammed     |
| Sonali Maharaj    | 816034459  | UI Design   | lillyem             |
| Sonia Mohammed    | 816040068  | Lead        | soniarosem          |


---


## Notes


- Used a clean, modern UI with high contrast purple tones for readability and aesthetic appeal.  
- Encountered challenges handling file uploads on free Render plans (ephemeral storage), which required creative handling of metadata and user feedback.  
- Leveraged team collaboration via GitHub and division of responsibilities across front-end, back-end, and DevOps.





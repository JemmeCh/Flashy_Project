<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://jemme-pages.notion.site/PHY3030-Projet-de-fin-d-tude-2ebbf452e3084609bec37e17ef400a1a?pvs=4">
    <img src="images-readme/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">PHY3030 - FLASHy Project</h3>

  <p align="center">
    DAQ - Prises et analyses de données avec un BCT et un digitizer DT5781 (CAEN) dans le contexte de physique médicale
    <br />
    <a href="https://github.com/Popitopi130/Flashy_Project/"><strong>Explorer les docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Popitopi130/Flashy_Project/">Voir démo</a>
    ·
    <a href="https://github.com/Popitopi130/Flashy_Project/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Popitopi130/Flashy_Project/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table des matières</summary>
  <ol>
    <li>
      <a href="#about-the-project">À propos du projet</a>
      <ul>
        <li><a href="#built-with">Possible grâce à</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Utilisation</a>
      <ul>
        <li><a href="#prerequisites">Prérequis</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributeurs.trices</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Reconnaissance</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## À propos du projet

[![Product Name Screen Shot][product-screenshot]](https://jemme-pages.notion.site/PHY3030-Projet-de-fin-d-tude-2ebbf452e3084609bec37e17ef400a1a?pvs=4)

La radiothérapie à ultra-haut débit de dose, ou radiothérapie FLASH, permet de traiter le cancer en délivrant des doses très élevées de radiation en quelques millisecondes. Les traitements pour le cancer actuels durent plusieurs minutes, et la radiothérapie FLASH, malgré un court temps d’exposition, semble être autant efficace en plus de réduire les dommages causées aux tissus sains avoisinant la ou les tumeurs. Le CHUM est équipé d’un appareil de radiothérapie FLASH, soit une première au Canada, et notre groupe de chercheur a la responsabilité de développer des nouveaux détecteurs compatibles avec cet appareil.

L’objectif du projet de fin de session est de créer un programme capable d’analyser les données enregistrées par les détecteurs dans le but de vérifier que le faisceau est la forme désirée. Le programme doit être capable de comprendre les signaux reçus, les analyser et former des graphiques décrivant les faisceaux détectés.

<!--
Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description` -->

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



### Possible grâce à
* [![matplotlib][matplotlib]][matplotlib-url]
* [![NumPy][numpy]][numpy-url]
* [tkinter][tkinter-url]
<!-- Pour mettre une librairie
* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
-->
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- GETTING STARTED -->
## Utilisation
<!-- 
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.
-->
### Prérequis
<!-- 
This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```
-->
### Installation
<!-- 
1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/Popitopi130/Flashy_Project.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin Popitopi130/Flashy_Project
   git remote -v # confirm the changes
   ```
-->
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
<!-- 
Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_
-->
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Analyse de données venant de CoMPASS (CSV)
    - [x] Affichage de graphes matplotlib
    - [x] Liste de résultat
    - [ ] Enregistrement des analyses
    - [ ] Calcul de dose
- [ ] Lecture directe du digitizer
    - [ ] À venir...

See the [open issues](https://github.com/Popitopi130/Flashy_Project/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- CONTRIBUTING -->
## Contributeurs.trices
<!-- 
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
-->
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

### Top Contributeurs.trices:

<a href="https://github.com/Popitopi130/Flashy_Project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Popitopi130/Flashy_Project" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License
<!-- 
Distributed under the MIT License. See `LICENSE.txt` for more information.
-->
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- CONTACT -->
## Contact
<!-- 
Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com
-->
Lien au projet: [https://github.com/Popitopi130/Flashy_Project](https://github.com/Popitopi130/Flashy_Project)

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Reconnaissances

* [Arthur Lalonde, mon superviseur de projet](https://recherche.umontreal.ca/english/our-researchers/professors-directory/researcher/is/in29955/)
* [Nicole St-Louis, la professeure du cours PHY3030](https://recherche.umontreal.ca/english/our-researchers/professors-directory/researcher/is/in15156/)
* [Arnaud Lessard, pour m'avoir aider avec NumPy](https://www.facebook.com/profile.php?id=100009397104882)
* [Readme.md template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[matplotlib]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
[matplotlib-url]: https://matplotlib.org/
[numpy]: https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue
[numpy-url]: https://numpy.org/
[tkinter-url]: https://docs.python.org/3/library/tkinter.html

[contributors-shield]: https://img.shields.io/github/contributors/Popitopi130/Flashy_Project.svg?style=for-the-badge
[contributors-url]: https://github.com/Popitopi130/Flashy_Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Popitopi130/Flashy_Project.svg?style=for-the-badge
[forks-url]: https://github.com/Popitopi130/Flashy_Project/network/members
[stars-shield]: https://img.shields.io/github/stars/Popitopi130/Flashy_Project.svg?style=for-the-badge
[stars-url]: https://github.com/Popitopi130/Flashy_Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/Popitopi130/Flashy_Project.svg?style=for-the-badge
[issues-url]: https://github.com/Popitopi130/Flashy_Project/issues
[license-shield]: https://img.shields.io/github/license/Popitopi130/Flashy_Project.svg?style=for-the-badge
[license-url]: https://github.com/Popitopi130/Flashy_Project/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/jean-emmanuel-chouinard/
[product-screenshot]: images-readme/FLASHy_0-2.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
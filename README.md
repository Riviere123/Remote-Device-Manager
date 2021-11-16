<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



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
  <a href="https://github.com/Riviere123/IoT-Central-Manager">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Device Management System</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/Riviere123/IoT-Central-Manager"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Riviere123/IoT-Central-Manager">View Demo</a>
    ·
    <a href="https://github.com/Riviere123/IoT-Central-Manager/issues">Report Bug</a>
    ·
    <a href="https://github.com/Riviere123/IoT-Central-Manager/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
### Installation

1. Download the code
2. alter the Server and Clients Config files to fit your systems IP and desired ports
3. Generate your Certificate with the GenerateCertificate.py
    This will generate a new certificate that fits the given information in the Config files
4. Run Server.py it will ask you for the password that you had set in the servers Config.py file
5. Run the client on a device, If configured correctly it will automaticly connect to the server.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Commands

<b>-Client Commands-</b>
These are commands that the client can send to the server.
1. set name - sets the clients name on the server.
2. set type - sets what type of device the client is.

<b>-Server Commands-</b>
These are commands you can run from the server

1. send (device name) (message) | Sends a message to the desired client

2. list or ls | lists all connected devices

3. run (device name) (message) | send a terminal command to the client and returns the results to the server

4. group create (group name) | Creates a group

5. group list or group ls | lists the groups and clients belonging to those groups

6. group add (group name) (device name) | adds the device to the group

7. group delete (group name) | deletes the group

8. group remove (group name) (device name) | removes the device from the group

9. group send (group name) (message) | Broadcasts the message to all devices in the group


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Feature 1
- [] Feature 2
- [] Feature 3
    - [] Nested Feature

See the [open issues](https://github.com/Riviere123/IoT-Central-Manager/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Curtis Redgate -  - Curtis.Redgate@gmail.com

Project Link: [https://github.com/Riviere123/IoT-Central-Manager](https://github.com/Riviere123/IoT-Central-Manager)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Riviere123/IoT-Central-Manager.svg?style=for-the-badge
[contributors-url]: https://github.com/Riviere123/IoT-Central-Manager/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Riviere123/IoT-Central-Manager.svg?style=for-the-badge
[forks-url]: https://github.com/Riviere123/IoT-Central-Manager/network/members
[stars-shield]: https://img.shields.io/github/stars/Riviere123/IoT-Central-Manager.svg?style=for-the-badge
[stars-url]: https://github.com/Riviere123/IoT-Central-Manager/stargazers
[issues-shield]: https://img.shields.io/github/issues/Riviere123/IoT-Central-Manager.svg?style=for-the-badge
[issues-url]: https://github.com/Riviere123/IoT-Central-Manager/issues
[license-shield]: https://img.shields.io/github/license/Riviere123/IoT-Central-Manager.svg?style=for-the-badge
[license-url]: https://github.com/Riviere123/IoT-Central-Manager/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/curtisredgate/
[product-screenshot]: images/screenshot.png

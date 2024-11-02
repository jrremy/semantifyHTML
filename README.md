# SemantifyHTML

This project is a web tool that aims to enhance the semantic quality of HTML code to promote accessibility and improve SEO (Search Engine Optimization). Built using a React frontend and Flask backend, it allows users to paste HTML code, load it from a URL, or upload an HTML file, and get a more semantic version of the code along with explanations for each change.

## Features

- **HTML Code Enhancement**: Users can input HTML code, load it from a URL, or upload an HTML file to receive a more semantic version that enhances accessibility and SEO.

- **Explanations for Changes**: Provides AI-generated explanations via OpenAI's API for each modification made to the HTML code, helping users understand the improvements.

- **Accessibility-Driven Recommendations**: Ensures the generated HTML follows best practices for screen readers and other assistive technologies, making web pages more inclusive.

- **SEO Optimization**: Analyzes and adjusts HTML elements to improve discoverability by search engines.

## Dependencies

### Backend

The backend of this project is built with Python and Flask, and relies on the following key dependencies:

- **Python**: Required to run the backend code. Make sure you have Python installed (preferably Python 3.8 or later).
- **Flask (3.0.3)**: A lightweight web framework used to build the backend server and handle HTTP requests.
- **Flask_Cors (4.0.1)**: Provides Cross-Origin Resource Sharing (CORS) support, allowing the frontend to securely communicate with the backend.
- **BeautifulSoup4 (4.12.3)**: Parses and navigates HTML content, enabling semantic analysis and transformation.
- **OpenAI (1.51.2)**: Used for natural language processing and other AI-driven tasks, enhancing the semantic analysis process.
- **Playwright (1.46.0)**: Facilitates headless browsing, which can be useful for dynamically loading and scraping HTML content.
- **Requests (2.32.3)**: Handles HTTP requests, allowing the backend to fetch HTML content from URLs provided by users.

### Frontend

The frontend is a React application bootstrapped with Vite, with dependencies focused on UI and state management:

- **React (18.3.1) and React DOM (18.3.1)**: Core libraries for building and rendering the UI components.
- **@mui/material (6.0.2) and @mui/icons-material (6.0.2)**: Material UI components and icons for a clean, responsive interface.
- **@emotion/react (11.13.3) and @emotion/styled (11.13.0)**: Provides powerful CSS-in-JS styling capabilities for a dynamic and customizable UI.
- **Axios (1.7.2)**: A promise-based HTTP client used to send requests from the frontend to the backend API.
- **React Spinners (0.14.1)**: A loading spinner component library, improving user experience during API calls.

### Development Dependencies

- **Vite (5.3.4)**: A fast frontend build tool that provides a streamlined development experience with fast module replacement.
- **ESLint (8.57.0)** and plugins: Used for code quality and consistency, ensuring adherence to best practices.
- **@vitejs/plugin-react (4.3.1)**: Adds support for React fast-refresh and JSX transformation, enhancing the development workflow.

import React from 'react';
import PropTypes from 'prop-types';
import "./FaceRecognitionGetStarted.css";
import WelcomeCard from './WelcomeCard/WelcomeCard';

const FaceDetectionService = () => {
  const SIGNUP_FORM_URL = 'https://forms.gle/15pNdt9f3BgL4nTh7';
  const currentYear = new Date().getFullYear();

  return (
    <main className="face-detection-service">
      <header>
        <h1>Face Detection Service</h1>
      </header>
      
      <WelcomeCard />
      
      <section className="service-description">
        <p>
          New to Face Detection Service? <br />
          Our service provides top-notch face detection to secure your identity.{' '}
          Sign up now to get registered!
        </p>
        <a 
          href={SIGNUP_FORM_URL} 
          target="_blank" 
          rel="noreferrer" 
          className="signup-button"
        >
          Sign Up
        </a>
      </section>

      <footer>
        <p>&copy; {currentYear} Face Detection Service</p>
      </footer>
    </main>
  );
};

WelcomeCard.propTypes = {
  // Add any props that WelcomeCard component accepts
};

FaceDetectionService.propTypes = {
  // Add any props if needed in the future
};

export default FaceDetectionService;
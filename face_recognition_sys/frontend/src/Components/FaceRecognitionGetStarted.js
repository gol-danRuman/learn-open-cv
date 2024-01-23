import React from 'react';
// import GoogleForm from './GoogleForm';
import "./FaceRecognitionGetStarted.css";
import WelcomeCard from './WelcomeCard/WelcomeCard';
import ModalComponent from './ModalComponent/CustomModal';

function GoogleForm() {
  return (
    <div className="google-form">
      <h2>Sign Up Form</h2>
      <p>This is a placeholder for the Google Form.</p>
    </div>
  );
}

function FaceDetectionService() {
  return (
    <div className="face-detection-service">
      <h1>Face Detection Service</h1>
      <WelcomeCard />
      {/* <ModalComponent/> */}
      <p>
        New to Face Detection Service? <br />
        Our service provides top-notch face detection to secure your identity.{' '}
        Sign up now to get registered!<br />
        <a href="https://forms.gle/15pNdt9f3BgL4nTh7" target='_blank' rel="noreferrer" className="signup-button" >Sign Up</a>
      </p>
      <footer>&copy; 2024 Face Detection Service</footer>
    </div>
  );
}



export default FaceDetectionService;
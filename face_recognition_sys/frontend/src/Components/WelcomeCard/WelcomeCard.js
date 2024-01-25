import React, { useEffect, useState } from 'react';
import { MdFace } from 'react-icons/md';
import { FaCamera } from "react-icons/fa";
import './WelcomeCard.css';
import FileInput from '../FileInputComponent/CustomFileInput';
import Webcam from 'react-webcam';

const LandingPage = (props) => {
  return (
    <div>
      <MdFace className="welcome-icon" />
      <h2 className="welcome-title">Welcome Back!</h2>
      <p className="welcome-text">Use our face detection service to enhance your security.</p>
      <button className="welcome-button" onClick={props.handleOptionOpen}><FaCamera className='camera-icon' />Initiate Face Detection</button>
    </div>
  );
};

const sendPhoto = async (file, setResponseData) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://127.0.0.1:8000https://face-recognition-sys-backend-api.onrender.com/verify', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      alert('Something went wrong');
      setResponseData(null);
      // throw new Error('Failed to send photo');
    }

    const data = await response.json();
    setResponseData(data);
    console.log('Photo upload successful:', data);
  } catch (error) {
    console.error('Error sending photo:', error);
  }
};

const LiveCameraPage = (props) => {
  return (
    <>
      <Webcam className="live-camera-card" imageSmoothing={props.isStreamLoading} />
      <div className='close-detect-btn'>
        <button style={{ width: "16rem" }} onClick={() => {
          console.log("Button clicked");
          props.setIsStreamLoading(false);
        }}>Close Camera</button>
        <button style={{ width: "16rem", marginLeft: "4rem" }} onClick={() => {
          console.log("Button clicked");
          props.setIsStreamLoading(false);
        }}>Detect</button>

      </div>

    </>
  )
}
const ImageSelectedPage = (props) => {

  const checkResponseData = () => {
    if (props.responseData != null && props.responseData.status === 'Face Detected') {
      props.setIsFaceDetected(true);
    }else{
      props.setIsFaceDetected(false);
    }
  }

  const handleDetect = async () => {
    console.log("Button clicked");
    await props.sendPhoto(props.image, props.setResponseData);
    console.log("After the photo send, reponse Data", props.re)
    checkResponseData();
    
    props.setIsImageSelected(false);
  };

  useEffect(() => {
    return () => {
      checkResponseData();
    };
  }, [props.isFaceDetected]);


  return (
    <>
      <div className='selected-image-card'>

        {props.image && <img className='selected-image' src={URL.createObjectURL(props.image)} alt="Selected Image" />}

        <div className='cancel-detect-btn'>
          <button style={{ marginTop: "1rem" }} onClick={() => {
            console.log("Button clicked");
            props.setIsImageSelected(false);
          }}>Cancel</button>
          <button style={{ marginTop: "1rem", marginLeft: "2rem" }} onClick={handleDetect}>Detect</button>
        </div>


      </div>
    </>
  )
}

const FaceDetectedPage = (props) => {


  return (
    <>
      <div className='result-card'>

        {props.image && <img className='selected-image' src={URL.createObjectURL(props.image)} alt="Selected Image" />}
        {props.responseData && (
          <> 
            <div> 
              {console.log(props.responseData)} 
              <b>Status: </b> {props.responseData.status} <br/>
              <b>Name:</b> {props.responseData.user_name}
            </div>
          
          </>)}
        <div className='reset-btn'>
          <button style={{ marginTop: "1rem" }} onClick={() => {
            console.log("Button clicked");
            props.setIsFaceDetected(false);
          }}>Reset</button>
        </div>


      </div>
    </>
  )
}

const OptionPage = (props) => {
  const [isStreamLoading, setIsStreamLoading] = useState(false);
  const [isImageSelected, setIsImageSelected] = useState(false);
  const [isFaceDetected, setIsFaceDetected] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [file, setFile] = useState(null);

  const handleButtonClick = () => {
    setIsStreamLoading(true);
    props.handleStreamLoad();
  };

  useEffect(() => {
    return () => {
      setIsStreamLoading(false);
    };
  }, []);

  return (
    <>
    {console.log(isStreamLoading, isImageSelected, isFaceDetected)}
    {
      isStreamLoading ? <LiveCameraPage isStreamLoading={isStreamLoading} setIsStreamLoading={setIsStreamLoading} /> :
        isImageSelected ? <>
          <ImageSelectedPage image={file} isImageSelected={isImageSelected} setIsImageSelected={setIsImageSelected} sendPhoto={sendPhoto} setIsFaceDetected={setIsFaceDetected} setResponseData={setResponseData} responseData={responseData} />
        </> :
          isFaceDetected ? <>
            <FaceDetectedPage image={file} setIsFaceDetected={setIsFaceDetected} responseData={responseData} />
          </> :

            <div className='option-card'>
              <h2>Choose an option</h2>
              <button onClick={handleButtonClick} disabled={isStreamLoading}>
                Live Camera
              </button>
              <FileInput setFile={setFile} setIsImageSelected={setIsImageSelected} />
            </div>


    }

    </>
  );
};


const WelcomeCard = () => {
  const [optionOpen, setOptionOpen] = useState(false);

  const handleOptionOpen = () => {
    setOptionOpen(true);
  };

  const handleStreamLoad = () => {
    // handle stream loading logic here
  };

  return (
    <div className="welcome-card">
      {optionOpen ? <OptionPage handleStreamLoad={handleStreamLoad} handleOptionOpen={handleOptionOpen} /> : <LandingPage handleOptionOpen={handleOptionOpen} />}
    </div>
  );
};

export default WelcomeCard;
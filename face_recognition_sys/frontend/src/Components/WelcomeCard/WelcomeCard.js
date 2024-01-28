import React, { useCallback, useEffect, useRef, useState } from 'react';
import { MdFace } from 'react-icons/md';
import { FaCamera } from "react-icons/fa";
import './WelcomeCard.css';
import FileInput from '../FileInputComponent/CustomFileInput';
import Webcam from 'react-webcam';
import MyLoader from '../MyLoader/MyLoader';

function convertBase64toBlob(base64String) {

  // Remove any prefix from the base64 string
  const base64Data = base64String.split(',')[1];

  // Decode the base64 string using the atob() function
  const binaryString = atob(base64Data);

  // Convert the binary string into an array of unsigned 8-bit integers
  const binaryArray = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    binaryArray[i] = binaryString.charCodeAt(i);
  }

  // Create a new ArrayBuffer object and a new Uint8Array view of the array buffer
  const arrayBuffer = binaryArray.buffer;

  // Create a new Blob object using the Blob() constructor
  return new Blob([arrayBuffer], { type: 'image/jpeg' });


}
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
    const response = await fetch('https://face-recognition-sys-backend-api.onrender.com/verify', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      alert('Something went wrong. Please Sign Up if you have not signed up yet.');
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
  const webcamRef = useRef(null);



  const handleDetect = async () => {
    console.log("Button clicked");
    const imageSrc = webcamRef.current.getScreenshot();

    props.setFile(convertBase64toBlob(imageSrc));


    props.setIsImageSelected(true);
    props.setIsStreamLoading(false);
  };


  return (
    <>
      <Webcam className="live-camera-card" imageSmoothing={props.isStreamLoading} screenshotFormat="image/jpeg" ref={webcamRef} />
      <div className='close-detect-btn'>
        <button style={{ width: "16rem" }} onClick={() => {
          console.log("Button clicked");
          props.setIsStreamLoading(false);
        }}>Close Camera</button>
        <button style={{ width: "16rem", marginLeft: "4rem" }} onClick={handleDetect}>Capture</button>

      </div>

    </>
  )
}
const ImageSelectedPage = (props) => {
  const [isLoading, setIsLoading] = useState(false);



  const checkResponseData = () => {
    if (props.responseData != null && props.responseData.status === 'Face Detected') {
      props.setIsFaceDetected(true);
    }
  }

  const handleDetect = async () => {
    setIsLoading(true);
    props.setIsFaceDetected(true);
    console.log("Button clicked");
    await props.sendPhoto(props.image, props.setResponseData);
    console.log("After the photo send, reponse Data", props.responseData);
    checkResponseData();

    props.setIsImageSelected(false);
    setIsLoading(false);
  };



  return (
    <>
      <div className='selected-image-card'>
        {isLoading ? <MyLoader /> :
          <>
            {props.image && <img className='selected-image' src={URL.createObjectURL(props.image)} alt="Selected Image" />}

            < div className='cancel-detect-btn'>
              <button style={{ marginTop: "1rem" }} onClick={() => {
                console.log("Button clicked");
                props.setIsImageSelected(false);
                props.setIsFaceDetected(false);
                props.setResponseData(null);
              }}>Cancel</button>
              <button style={{ marginTop: "1rem", marginLeft: "2rem" }} onClick={handleDetect} disabled={isLoading}>Detect</button>
            </div>
          </>
        }


      </div >
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
              <b>Status: </b> {props.responseData.status ? props.responseData.status : "Unknown" } <br />
              <b>Name:</b> {props.responseData.user_name ? props.responseData.user_name : "Unknown"}
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
        isStreamLoading ? <LiveCameraPage isStreamLoading={isStreamLoading} setIsStreamLoading={setIsStreamLoading} setIsImageSelected={setIsImageSelected} image={file} setFile={setFile} sendPhoto={sendPhoto} setIsFaceDetected={setIsFaceDetected} setResponseData={setResponseData} responseData={responseData} /> :
          isImageSelected ? <>
            <ImageSelectedPage image={file} isImageSelected={isImageSelected} setIsImageSelected={setIsImageSelected} sendPhoto={sendPhoto} setIsFaceDetected={setIsFaceDetected} setResponseData={setResponseData} responseData={responseData} />
          </> :
            isFaceDetected ? <>
              <FaceDetectedPage image={file} setIsFaceDetected={setIsFaceDetected} responseData={responseData} />
            </> :

              <div className='option-card'>
                <h2>Choose an option</h2>
                {/* <button onClick={handleButtonClick} disabled={isStreamLoading}>
                  Live Camera
                </button> */}
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
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { MdFace } from 'react-icons/md';
import { FaCamera } from "react-icons/fa";
import './WelcomeCard.css';
import FileInput from '../FileInputComponent/CustomFileInput';
import Webcam from 'react-webcam';
import MyLoader from '../MyLoader/MyLoader';

const convertBase64toBlob = (base64String) => {
  try {
    const base64Data = base64String.split(',')[1];
    const binaryString = atob(base64Data);
    const buffer = new ArrayBuffer(binaryString.length);
    const view = new Uint8Array(buffer);
    
    for (let i = 0; i < binaryString.length; i++) {
      view[i] = binaryString.charCodeAt(i);
    }

    const timestamp = new Date().getTime();
    const fileName = `captured_image_${timestamp}.jpg`;

    const file = new File([buffer], fileName, {
      type: 'image/jpeg',
      lastModified: Date.now()
    });

    return file;
  } catch (error) {
    console.error('Error converting base64 to blob:', error);
    throw new Error('Failed to process captured image');
  }
};

const API = {
  async verifyPhoto(file, setResponseData) {
    try {
      const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
      
      const formData = new FormData();
      
      if (file instanceof File) {
        formData.append('file', file, file.name);
      } else if (file instanceof Blob) {
        const timestamp = new Date().getTime();
        const fileName = `captured_image_${timestamp}.jpg`;
        
        const fileFromBlob = new File([file], fileName, {
          type: 'image/jpeg',
          lastModified: Date.now()
        });
        
        formData.append('file', fileFromBlob, fileName);
      } else {
        throw new Error('Invalid file format');
      }

      const response = await fetch('http://127.0.0.1:8000/verify', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
        body: formData
      });

      const data = await response.json();
      
      if (!response.ok) {
        setResponseData({ 
          error: data.message || data.error || 'Please upload a photo with a clear image where face, eyes, and ears are properly visible'
        });
        return null;
      }

      setResponseData(data);
      return data;
    } catch (error) {
      console.error('Error verifying photo:', error);
      setResponseData({ 
        error: 'Please upload a photo with a clear image where face, eyes, and ears are properly visible'
      });
      return null;
    }
  }
};

const LandingPage = ({ handleOptionOpen }) => (
  <div>
    <MdFace className="welcome-icon" />
    <h2 className="welcome-title">Welcome Back!</h2>
    <p className="welcome-text">Use our face detection service to enhance your security.</p>
    <button className="welcome-button" onClick={handleOptionOpen}>
      <FaCamera className='camera-icon' />Initiate Face Detection
    </button>
  </div>
);

const LiveCameraPage = ({ 
  setFile, 
  setIsImageSelected, 
  setIsStreamLoading, 
  isStreamLoading,
  setIsFaceDetected,
  setResponseData 
}) => {
  const webcamRef = useRef(null);

  const handleCapture = useCallback(async () => {
    try {
      const imageSrc = webcamRef.current?.getScreenshot();
      if (imageSrc) {
        const imageFile = await convertBase64toBlob(imageSrc);
        setFile(imageFile);
        setIsStreamLoading(false);
        setIsImageSelected(true);
      }
    } catch (error) {
      console.error('Error capturing image:', error);
      alert('Failed to capture image. Please try again.');
    }
  }, [setFile, setIsImageSelected, setIsStreamLoading]);

  return (
    <>
      <Webcam 
        className="live-camera-card" 
        imageSmoothing={isStreamLoading} 
        screenshotFormat="image/jpeg" 
        ref={webcamRef} 
        mirrored={true}
        width={400}
        height={300}
      />
      <div className='close-detect-btn'>
        <button 
          className="action-button"
          onClick={() => setIsStreamLoading(false)}
        >
          Close Camera
        </button>
        <button 
          className="action-button detect-button"
          onClick={handleCapture}
        >
          Capture Image
        </button>
      </div>
    </>
  );
};

const ImageSelectedPage = ({ image, setIsImageSelected, setIsFaceDetected, setResponseData, responseData }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleDetect = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await API.verifyPhoto(image, setResponseData);
      if (result) {
        setIsFaceDetected(true);
        setIsImageSelected(false);
      }
    } finally {
      setIsLoading(false);
    }
  }, [image, setResponseData, setIsFaceDetected, setIsImageSelected]);

  return (
    <div className='selected-image-card'>
      {isLoading ? (
        <MyLoader />
      ) : (
        <div>
          {image && (
            <div className="preview-container">
              <img 
                className='selected-image' 
                src={URL.createObjectURL(image)} 
                alt="Selected" 
              />
              <div className='image-actions'>
                <button 
                  className="action-button detect-button"
                  onClick={handleDetect} 
                  disabled={isLoading}
                >
                  Detect
                </button>
              </div>
            </div>
          )}
          <div className="error-message">
            {isLoading && <p>Processing image...</p>}
            {responseData?.error && (
              <p style={{ 
                color: 'red',
                textAlign: 'center',
                padding: '10px',
                margin: '10px 0'
              }}>
                {responseData.error}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const FaceDetectedPage = ({ image, responseData }) => (
  <div className='result-card'>
    {image && (
      <img 
        className='selected-image' 
        src={URL.createObjectURL(image)} 
        alt="Selected" 
      />
    )}
    {responseData && responseData.user_data && (
      <div className="user-details">
        <h3>User Details</h3>
        <div className="detail-row">
          <b>Name:</b> {responseData.user_data.name}
        </div>
        <div className="detail-row">
          <b>Email:</b> {responseData.user_data.email}
        </div>
        <div className="detail-row">
          <b>Contact:</b> {responseData.user_data.contact}
        </div>
      </div>
    )}
  </div>
);

const OptionPage = ({ isStreamOpen, setIsStreamOpen, handleBack, initialFile, initialImageSelected }) => {
  const [state, setState] = useState({
    isStreamLoading: isStreamOpen,
    isImageSelected: initialImageSelected,
    isFaceDetected: false,
    responseData: null,
    file: initialFile
  });

  const setStateValue = useCallback((key, value) => {
    setState(prev => ({ ...prev, [key]: value }));
  }, []);

  useEffect(() => {
    setStateValue('isStreamLoading', isStreamOpen);
  }, [isStreamOpen, setStateValue]);

  useEffect(() => {
    if (initialFile) {
      setStateValue('file', initialFile);
      setStateValue('isImageSelected', true);
    }
  }, [initialFile, setStateValue]);

  const renderContent = () => {
    if (state.isStreamLoading) {
      return (
        <>
          <LiveCameraPage 
            isStreamLoading={state.isStreamLoading}
            setIsStreamLoading={(value) => {
              setStateValue('isStreamLoading', value);
              setIsStreamOpen(value);
            }}
            setIsImageSelected={(value) => setStateValue('isImageSelected', value)}
            setFile={(value) => setStateValue('file', value)}
            setIsFaceDetected={(value) => setStateValue('isFaceDetected', value)}
            setResponseData={(value) => setStateValue('responseData', value)}
          />
          <button className="back-button" onClick={handleBack}>
            Back to Options
          </button>
        </>
      );
    }

    if (state.isImageSelected) {
      return (
        <>
          <ImageSelectedPage 
            image={state.file}
            setIsImageSelected={(value) => setStateValue('isImageSelected', value)}
            setIsFaceDetected={(value) => setStateValue('isFaceDetected', value)}
            setResponseData={(value) => setStateValue('responseData', value)}
            responseData={state.responseData}
          />
          <button className="back-button" onClick={handleBack}>
            Back to Options
          </button>
        </>
      );
    }

    if (state.isFaceDetected) {
      return (
        <>
          <FaceDetectedPage 
            image={state.file}
            responseData={state.responseData}
          />
          <button className="back-button" onClick={handleBack}>
            Back to Options
          </button>
        </>
      );
    }

    return (
      <div className='option-card'>
        <h2>Choose an option</h2>
        <FileInput 
          setFile={(value) => setStateValue('file', value)}
          setIsImageSelected={(value) => setStateValue('isImageSelected', value)}
        />
        <button className="back-button" onClick={handleBack}>
          Back to Options
        </button>
      </div>
    );
  };

  return <>{renderContent()}</>;
};

const WelcomeCard = () => {
  const [optionOpen, setOptionOpen] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [isStreamOpen, setIsStreamOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleBack = useCallback(() => {
    setOptionOpen(false);
    setIsStreamOpen(false);
    setShowOptions(true);
    setSelectedFile(null);
  }, []);

  const handleOptionOpen = useCallback(() => {
    setShowOptions(true);
  }, []);

  const handleCameraOption = useCallback(() => {
    setIsStreamOpen(true);
    setOptionOpen(true);
  }, []);

  const handleFileOption = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleFileChange = useCallback((event) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      
      const imageFile = new File([file], file.name, {
        type: file.type,
        lastModified: file.lastModified
      });
      
      setSelectedFile(imageFile);
      setOptionOpen(true);
    }
  }, [setOptionOpen]);

  const renderOptions = () => (
    <div className="options-container">
      <h2 className="welcome-title">Choose an Option</h2>
      <div className="options-buttons">
        <button 
          className="option-button"
          onClick={handleFileOption}
        >
          <FaCamera className='camera-icon' />
          Upload Photo
        </button>
        <button 
          className="option-button"
          onClick={handleCameraOption}
        >
          <FaCamera className='camera-icon' />
          Use Camera
        </button>
      </div>
      <button 
        className="back-button"
        onClick={() => setShowOptions(false)}
      >
        Back
      </button>
    </div>
  );

  const renderContent = () => {
    if (optionOpen) {
      return (
        <OptionPage 
          isStreamOpen={isStreamOpen}
          setIsStreamOpen={setIsStreamOpen}
          handleBack={handleBack}
          initialFile={selectedFile}
          initialImageSelected={!!selectedFile}
        />
      );
    }

    if (showOptions) {
      return renderOptions();
    }

    return <LandingPage handleOptionOpen={handleOptionOpen} />;
  };

  return (
    <div className="welcome-card">
      {renderContent()}
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
        accept="image/*"
      />
    </div>
  );
};

export default WelcomeCard;
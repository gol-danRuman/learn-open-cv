import logo from './logo.svg';
import background from './assets/background.jpg';
import './App.css';
import ImageSearchForm from "./Components/ImageSearchForm/ImageSearchForm";
// import FaceDetect from "./Components/FaceDetect/FaceDetect";
import FaceDetectionService from './Components/FaceRecognitionGetStarted';
function App() {
  return (
    <div className="App">
      
      <FaceDetectionService/>
      {/* <ImageSearchForm/> */}
      {/* <FaceDetect /> */}
      {/* <FaceRecognition/> */}
    </div>
  );
}

export default App;

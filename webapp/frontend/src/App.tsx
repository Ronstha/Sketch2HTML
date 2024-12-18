import { BrowserRouter, Route, Routes } from "react-router";
import Home from "./pages/Home";

function App() {

return(
  <div className="w-screen min-h-screen py-[20px] px-[50px] bg-white">
  
  <BrowserRouter>
  <Routes>
    <Route path="/" element={<Home/>}/>
  </Routes>
  </BrowserRouter>
  </div>
  
)
}

export default App

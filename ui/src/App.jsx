import { BrowserRouter, Routes, Route } from "react-router-dom";
import Terminal from "./components/Terminal"
import Login from "./components/Login";

function App() {

  return (
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<Terminal />} />
				<Route path='/login' element={<Login />} />
			</Routes>
		</BrowserRouter>
  )
}

export default App

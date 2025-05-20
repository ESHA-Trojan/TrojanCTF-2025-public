import React from "react";
import { useNavigate } from "react-router-dom";

const Nav = () => {
	const navigate = useNavigate();

	const signOut = () => {
		localStorage.removeItem("_id");
		navigate("/");
	};
	return (
		<nav className='navbar'>
			<h2>UltraH4x F0rum: by h4x0rz, for h4x0rz</h2>

			<div className='navbarRight'>
				<button onClick={signOut}>Sign out</button>
			</div>
		</nav>
	);
};

export default Nav;

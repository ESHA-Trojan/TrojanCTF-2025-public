import React, { useEffect, useState, process } from "react";
import Likes from "../utils/Likes";
import Comments from "../utils/Comments";
import { useNavigate } from "react-router-dom";
import Nav from "./Nav";

const Home = () => {
    const [thread, setThread] = useState("");
    const [threadList, setThreadList] = useState([]);
    const [endorsements_or_flag, setEndorsements] = useState("You currently have 0 endorsements");
    const navigate = useNavigate();
    const userID = localStorage.getItem("_id");


    useEffect(() => {
        fetch(process.env.REACT_APP_SERVER + "/api/check-login", {
            method: "POST",
            body: JSON.stringify({ userID }),
            headers: { "Content-Type": "application/json" },
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.loggedout) {
                    navigate("/");
                }
            })
            .catch((err) => console.error(err));

        if (!userID) {
            navigate("/");
        } else {
            fetch(process.env.REACT_APP_SERVER + "/api/all/threads", {
                method: "POST",
                body: JSON.stringify({ userID }),
                headers: { "Content-Type": "application/json" },
            })
                .then((res) => res.json())
                .then((data) => {
                    setThreadList(data.threads)
                })
                .catch((err) => console.error(err));

                fetch(process.env.REACT_APP_SERVER + "/api/user/endorsements", {
                    method: "POST",
                    body: JSON.stringify({ userID }),
                    headers: { "Content-Type": "application/json" },
                })
                    .then((res) => res.json())
                    .then((data) => {
                        setEndorsements("You currently have " + data.endorsements.toString() + " endorsements.")
                    })
                    .catch((err) => console.error(err))
            
        }
    }, [userID, navigate]);

    function endorseUser(user) {
        fetch(process.env.REACT_APP_SERVER + "/api/endorse", {
            method: "POST",
            body: JSON.stringify({ userID: user, endorserID: localStorage.getItem("_id") }),
            headers: { "Content-Type": "application/json" },
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.error_message) {
                    alert(data.error_message);
                } else {
                    alert("User endorsed successfully!");
                }
            })
            .catch((err) => console.error(err));
    };

	const createThread = () => {
        let userID = localStorage.getItem("_id")
		fetch(process.env.REACT_APP_SERVER + "/api/create/thread", {
			method: "POST",
			body: JSON.stringify({
				thread,
				user: userID,
			}),
			headers: {
				"Content-Type": "application/json",
			},
		})
			.then((res) => res.json())
			.then((data) => {
				setThreadList(data.threads);
			})
			.catch((err) => console.error(err));
	};
	const handleSubmit = (e) => {
		e.preventDefault();
		createThread();
		setThread("");
	};

    return (
        <>
            <Nav />
            <main className='home'>
                <p classname='endorsements'>{endorsements_or_flag}</p>
                <h2 className='homeTitle'>Create a Thread</h2>
                <form className='homeForm' onSubmit={handleSubmit}>
                    <div className='home__container'>
                        <label htmlFor='thread'>Title / Description</label>
                        <input
                            type='text'
                            name='thread'
                            required
                            value={thread}
                            onChange={(e) => setThread(e.target.value)}
                        />
                    </div>
                    <button className='homeBtn'>CREATE THREAD</button>
                </form>

                <div className='thread__container'>
					{threadList.map((thread) => (
						<div className='thread__item' key={thread.id}>
							<p>{thread.title}</p>
							<button className='endorseBtn' onClick={() => endorseUser(thread.userID)}>Endorse Creator</button>
							<div className='react__container'>
								<Likes numberOfLikes={thread.likes.length} threadId={thread.id} />
								<Comments numberOfComments={thread.replies.length} threadId={thread.id} title={thread.title} />
							</div>
						</div>
					))}
                </div>
            </main>
        </>
    );
};

export default Home;
const express = require("express");
const cors = require("cors");
const app = express();
const PORT = 4000;

const {
	RegExpMatcher,
	TextCensor,
	englishDataset,
	englishRecommendedTransformers,
} = require('obscenity');

const matcher = new RegExpMatcher({
	...englishDataset.build(),
	...englishRecommendedTransformers,
});

const censor = new TextCensor();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors());

const users = [{ id: "ozcxD11QzO99DNzME0YZ", email: "admin", password: "APeXHTANtzFMaAVpb0m5", username: "admin", endorsements: new Array(500).fill(0) }];
const threadList = [{id: "info",
    title: "General info 🤓",
    userId: "admin",
    replies: [{ name: "admin", text: "Site is currently under maintenance (expect loss of functionality and frequent resets 🤪). If the site doesnt work, refresh."}, { name: "admin", text: "For the l33t5 among you (over 500 endorsements): A cool project is in the works 😎, stay tuned! 😉"}],
    likes: [],
	hidden: false,
	},
	{
		id: "hidden-thread-x7UNfYXkOO",
		title: "🔥 Exclusive Hacker Lounge 🔥",
		userId: "admin",
		replies: [
			{name: "trojan", text: "Trojan{1_c4N_5Cr1pT_0r_I_c4N_cl1CK}"},
			{name: "admin", text: "Now that the n00bs don't hear us, you check out the awesome h4xcoin cryptocurrency i'm developing."},
			{name: "admin", text: "The coin is hosted on a chain of blockchains (blockchainchain 🤪), one for every user."},
			{name: "admin", text: "You can interact with the h4xcoin api on https://chain.chall.trojanc.tf, here's the api key: zChWbFITvM4HSPFcshkQ."},
			{name: "admin", text: "Check out /info on the api for info about all the available endpoints."},
			{name: "admin", text: "Registration is tied to your userID on the forums, but you can pick any username you want."},
			{name: "admin", text: 'You can find me on there as "admin". I will hook you up woth 10 h4xcoin when you register. 🤑'},
			{name: "admin", text: 'Try sending some small amount of h4xcoin to "testing" to get acquainted with how everything works.'},
			{name: "admin", text: "If you find a vulnerability or an opsec fail (Oops 😅) make sure to tell me!"}
		],
		likes: [],
		hidden: true,
	}];

const generateID = () => Math.random().toString(36).substring(2, 10);

app.post("/api/login", (req, res) => {
	const { email, password } = req.body;
	if (email === undefined || password === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let result = users.filter(
			(user) => user.email === email && user.password === password
		);
	
		if (result.length !== 1) {
			return res.json({
				error_message: "Incorrect credentials",
			});
		}
	
		res.json({
			message: "Login successful",
			id: result[0].id,
		});
	}
});

app.post("/api/register", async (req, res) => {
    const { email, password, username } = req.body;
	if (email === undefined || password === undefined || username === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		const id = generateID();
		const result = users.filter((user) => user.email === email || user.username === username );
	
		const matches = matcher.getAllMatches(username);
	
		let specialChars =/[`!@#$%^&*()_\-+=\[\]{};':"\\|,.<>\/?~ ]/;
	
		if (matches.length > 0) {
			res.json({ error_message: "Username contains profanities!" })
		} else if (username.length > 10) {
			res.json({ error_message: "Username is too long!" })
		} else if (specialChars.test(username)) {
			res.json({ error_message: "Only letters and numbers are allowed in the username!" })
		} else if (email.length > 30) {
			res.json({ error_message: "Email is too long!" })
		} else if (password.length > 20) {
			res.json({ error_message: "Password is too long!" })
		} else if (result.length === 0) {
			const newUser = { id, email, password, username, endorsements: [] };
			users.push(newUser);
	
			return res.json({ message: "Account created successfully!" });
		} else {
			res.json({ error_message: "User already exists" });
		}
	}
});

app.post("/api/create/thread", async (req, res) => {
	const { thread, user } = req.body;
	if (thread === undefined || user === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let threadID = generateID();

		const matches = matcher.getAllMatches(thread);

		let userob = users.find((userob) => userob.id === user);

		if (userob === undefined) {
			res.json({ error_message: "User does not exist." });
		} else {
			threadList.unshift({
				id: threadID,
				title: (censor.applyTo(thread, matches).substring(0, 20)).replace(/[^a-zA-Z0-9 .,!()]/g, ''),
				userID: user,
				replies: [],
				likes: [],
				hidden: false,
			});
		
			if (userob && userob.endorsements.length >= 500) {
				res.json({ message: "Thread created successfully!", threads: threadList });
			} else {
				res.json({ message: "Thread created successfully!", threads: threadList.filter((thread) => thread.hidden === false) });
			}
		}
	}
});

app.post("/api/all/threads", (req, res) => {
	const { userID } = req.body;
	if (userID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let user = users.find((user) => user.id === userID);
		if (user === undefined) {
			res.json({
				error_message: "User does not exist.",
			});
		} else {
			if (user && user.endorsements.length >= 500) {
				res.json({ threads: threadList });
			} else {
				res.json({ threads: threadList.filter((thread) => thread.hidden === false) });
			}	
		}
	}
});

app.post("/api/user/endorsements", (req, res) => {
	const { userID } = req.body;
	if (userID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let user = users.find((user) => user.id === userID);

		if (user === undefined) {
			res.json({
				error_message: "User does not exist.",
			});
		} else {
			res.json({ endorsements: user.endorsements.length });
		}
	}
});

app.post("/api/thread/like", (req, res) => {
	const { threadID, userID } = req.body;
	if (userID === undefined || threadID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		const result = threadList.filter((thread) => thread.id === threadID);
		if (result.length !== 1) {
			res.json({
				error_message: "Thread does not exist.",
			});
		} else {
			const threadLikes = result[0].likes;
			const authenticateReaction = threadLikes.filter((user) => user === userID);
		
			if (authenticateReaction.length === 0) {
				threadLikes.push(userID);
				return res.json({
					message: "You've reacted to the post!",
				});
			}
			res.json({
				error_message: "You can only react once!",
			});
		}
	}
});

app.post("/api/endorse", (req, res) => {
    const { userID, endorserID } = req.body;
	if (userID === undefined || endorserID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		if (userID === endorserID) {
			return res.json({ error_message: "You cannot endorse yourself!" });
		}

		let user = users.find((user) => user.id === userID);
		if (!user) {
			return res.json({ error_message: "User not found" });
		} else {
			if (!user.endorsements.includes(endorserID)) {
				user.endorsements.push(endorserID);
				return res.json({
					message: "User endorsed successfully!",
				});
			}
			res.json({
				error_message: "You can only endorse a user once!",
			});
		}
	}
});

app.post("/api/check-login", (req, res) => {
    const { userID } = req.body;
	if (userID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let result = users.filter(
			(user) => user.id === userID
		);

		if (result.length !== 1) {
			res.json({
				loggedout: true,
			});
		} else {
			res.json({
				loggedout: false,
			});
		}
	}
});

app.post("/api/check-id", (req, res) => {
    const { userID } = req.body;
	if (userID === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		let result = users.filter(
			(user) => user.id === userID
		);


		if (result.length !== 1) {
			res.json({
				result: "false",
			});
		} else {
			res.json({
				result: "true",
			});
		}
	}
});

app.post("/api/thread/replies", (req, res) => {
	const { id } = req.body;
	if (id === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		const result = threadList.filter((thread) => thread.id === id);
		if (result.length !== 1) {
			res.json({
				error_message: "Thread does not exist.",
			});
		} else {
			res.json({
				replies: result[0].replies,
				title: result[0].title,
			});
		}
	}
});

app.post("/api/create/reply", async (req, res) => {
	const { id, userID, reply } = req.body;
	if (userID === undefined || id === undefined || reply === undefined) {
		res.json({ error_message: "Parameters missing or malformed request" });
	} else {
		const result = threadList.filter((thread) => thread.id === id);
		const username = users.filter((user) => user.id === userID);

		if (result.length !== 1 || username.length !== 1) {
			res.json({
				error_message: "User or thread does not exist.",
			});
		} else {
			const matches = matcher.getAllMatches(reply);

			if (result[0].id === "info" || result[0].id === "hidden-thread-x7UNfYXkOO") {
				res.json({
					message: "Replies deactivated during maintenance.",
				});
			} else {
				result[0].replies.unshift({ name: username[0].username, text: (censor.applyTo(reply, matches).substring(0, 100)).replace(/[^a-zA-Z0-9 .,!()]/g, '') });
	
				res.json({
					message: "Response added successfully!",
				});
			}
		}
	}
});

app.listen(PORT, () => {
	console.log(`Server listening on ${PORT}`);
});

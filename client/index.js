
const express = require('express');
const app = express();

app.use(express.static(__dirname));

// Configure view engine to render EJS templates.
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.use(express.static(__dirname + "/public"))

// const bodyParser = require('body-parser');
// const expressSession = require('express-session')({
//   secret: 'blah3blah2blah1',
//   resave: false,
//   saveUninitialized: false
// });

// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: true }));
// app.use(expressSession);

// Configure view engine to render EJS templates.
// app.set('views', __dirname + '/views');
// app.set('view engine', 'ejs');

// app.use(express.static(__dirname + "/public"))

/* FIREBASE */
// const initializeApp = require('firebase/app').initializeApp // if this doesn't work, need:
// //const initializeApp = require('https://www.gstatic.com/firebasejs/9.6.6/firebase-app.js') 
// const db = require('firebase/firestore').getFirestore
// const auth = require('firebase/auth').getAuth
// const signInWithEmailAndPassword = require('firebase/auth').signInWithEmailAndPassword

// // Your web app's Firebase configuration
// // For Firebase JS SDK v7.20.0 and later, measurementId is optional
// const firebaseConfig = {
//   apiKey: "AIzaSyDvTm-acSGot4FoUtVaR1_oDHopAE-tIvk",
//   authDomain: "tea-point-75f3a.firebaseapp.com",
//   projectId: "tea-point-75f3a",
//   storageBucket: "tea-point-75f3a.appspot.com",
//   messagingSenderId: "110478911515",
//   appId: "1:110478911515:web:ffc62f27b33347c7c5f0be",
//   measurementId: "G-8JB341WWHE"
// };

// // Initialize Firebase
// const firebaseApp = initializeApp(firebaseConfig);

// app.post('/',
//     function(req,res){
//         var email = req.body.email
//         var password = req.body.password
//         // sign in for email and password
//         signInWithEmailAndPassword(auth, email, password)
//             .then((userCredential) => {
//                 const user = userCredential.user;
//         })
//             .catch((error) => {
//                 const errorCode = error.code;
//                 const errorMessage = error.message;
//         });

//     })


/* ROUTES */

app.get('/', (req, res) => {
    res.render('login');
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.get('/dashboard', (req, res) => {
    res.render('dashboard');
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log('App listening on port ' + port));


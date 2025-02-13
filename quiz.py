import streamlit as st
import streamlit.components.v1 as components

def display_quiz():
    quiz_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: system-ui, -apple-system, sans-serif;
                background-color: #0f1116;  /* Changé en noir */
                color: white;
                min-height: 100%;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding: 1rem;
            }
            
            /* Classes utilitaires */
            .w-full {
                width: 100%;
            }
            
            /* Couleurs de fond */
            .bg-slate-900 {
                background-color: #0f1116;  /* Changé en noir */
            }
            .bg-slate-800 {
                background-color: #1e293b;
            }
            .bg-slate-700 {
                background-color: #334155;
            }
            .bg-slate-600 {
                background-color: #475569;
            }
            .bg-blue-500 {
                background-color: #3b82f6;
            }
            .bg-black {
                background-color: #0f1116;  /* Changé en noir */
            }
            
            /* Couleurs de texte */
            .text-white {
                color: white;
            }
            .text-slate-300 {
                color: #cbd5e1;
            }
            .text-slate-200 {
                color: #e2e8f0;
            }
            .text-red-400 {
                color: #f87171;
            }
            .text-purple-400 {
                color: #c084fc;
            }
            .text-blue-400 {
                color: #60a5fa;
            }
            .text-green-400 {
                color: #4ade80;
            }
            .text-yellow-400 {
                color: #facc15;
            }
            
            /* Tailles de texte */
            .text-sm {
                font-size: 0.875rem;
                line-height: 1.25rem;
            }
            .text-lg {
                font-size: 1rem;
                line-height: 1.5rem;
            }
            .text-xl {
                font-size: 1.125rem;
                line-height: 1.75rem;
            }
            
            /* Styles de texte */
            .font-semibold {
                font-weight: 600;
            }
            .leading-relaxed {
                line-height: 1.625;
            }
            
            /* Espacement */
            .p-6 {
                padding: 1.5rem;  /* Augmenté de 0.75rem à 1.5rem */
            }
            .p-4 {
                padding: 0.75rem;
            }
            .p-3 {
                padding: 0.5rem;
            }
            .pb-2 {
                padding-bottom: 0.5rem;
            }
            .mb-6 {
                margin-bottom: 1.5rem;  /* Augmenté de 0.5rem à 1.5rem */
            }
            .mb-3 {
                margin-bottom: 0.75rem;
            }
            .mt-1 {
                margin-top: 0.25rem;
            }
            .mt-4 {
                margin-top: 1rem;
            }
            
            /* Flex */
            .flex {
                display: flex;
            }
            .flex-1 {
                flex: 1 1 0%;
            }
            .flex-shrink-0 {
                flex-shrink: 0;
            }
            .items-center {
                align-items: center;
            }
            .items-start {
                align-items: flex-start;
            }
            .gap-2 {
                gap: 0.5rem;
            }
            .gap-3 {
                gap: 0.75rem;
            }
            
            /* Espacement vertical */
            .space-y-6 > * + * {
                margin-top: 1.5rem;  /* Augmenté de 0.75rem à 1.5rem */
            }
            .space-y-3 > * + * {
                margin-top: 0.5rem;
            }
            .space-y-1 > * + * {
                margin-top: 0.25rem;
            }
            
            /* Bordures et coins arrondis */
            .rounded-lg {
                border-radius: 0.5rem;
            }
            .rounded-full {
                border-radius: 9999px;
            }
            
            /* Hauteurs */
            .h-1 {
                height: 0.25rem;
            }
            .h-auto {
                height: auto;
            }
            
            /* Transitions */
            .transition-all {
                transition: all 0.2s ease-in-out;
            }
            
            /* Composants spécifiques */
            .card {
                border-radius: 0.5rem;
                padding: 1rem;  /* Augmenté de 0.5rem à 1rem */
                width: 100%;
                max-width: 100%;
                margin: 0.5rem auto;  /* Augmenté de 0.25rem à 0.5rem */
                background-color: #0f1116;  /* Changé en noir */
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            
            .card-header {
                margin-bottom: 1rem;
            }
            
            .button {
                width: 100%;
                padding: 1.25rem;  /* Augmenté de 0.75rem à 1.25rem */
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                cursor: pointer;
                transition: background-color 0.2s;
                font-size: 1.1rem;  /* Légèrement plus grand */
                text-align: left;
                margin-bottom: 1rem;  /* Augmenté de 0.5rem à 1rem */
            }
            
            .button:hover {
                background-color: #475569;
            }
            
            /* Icônes */
            .icon {
                width: 1.5rem;
                height: 1.5rem;
                flex-shrink: 0;
            }
            
            .chevron-icon {
                width: 1rem;
                height: 1rem;
                margin-right: 0.5rem;
                flex-shrink: 0;
            }
            
            /* Barre de progression */
            .progress-bar {
                width: 100%;
                height: 0.25rem;
                background-color: #334155;
                border-radius: 9999px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                background-color: #3b82f6;
                border-radius: 9999px;
                transition: width 0.3s ease;
            }

            @media (max-width: 640px) {
                .card {
                    margin: 0;
                    padding: 1rem;
                }
                
                body {
                    padding: 1rem;
                }
            }

            /* Ajoutez ces styles pour le conteneur racine */
            #quiz-root {
                width: 100%;
                max-width: 1200px;
                margin: 0 auto;
                height: auto;
            }

            /* Ajoutez ces styles pour le conteneur des résultats */
            .results-container {
                max-height: 572px;  /* Augmenté de 520px à 572px (10% de plus) */
                overflow-y: auto;
                padding-right: 0.75rem;
            }

            /* Style pour la barre de défilement */
            .results-container::-webkit-scrollbar {
                width: 8px;
            }

            .results-container::-webkit-scrollbar-track {
                background: #1e293b;
                border-radius: 4px;
            }

            .results-container::-webkit-scrollbar-thumb {
                background: #475569;
                border-radius: 4px;
            }

            .results-container::-webkit-scrollbar-thumb:hover {
                background: #64748b;
            }

            .hover\:bg-slate-600:hover {
                background-color: #475569;
            }
        </style>
    </head>
    <body>
        <div id="quiz-root"></div>
        <script type="text/babel">
            // Composants d'icônes
            const Star = () => (
                <svg className="icon text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
            );

            const Heart = () => (
                <svg className="icon text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
            );

            const Brain = () => (
                <svg className="icon text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.04-.2 2.5 2.5 0 0 1 1-4.74 2.5 2.5 0 0 1 1.5-4.5 2.5 2.5 0 0 1 1.5-4.5Z"/>
                    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.04-.2 2.5 2.5 0 0 0-1-4.74 2.5 2.5 0 0 0-1.5-4.5 2.5 2.5 0 0 0-1.5-4.5Z"/>
                </svg>
            );

            const Code = () => (
                <svg className="icon text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="16 18 22 12 16 6"/>
                    <polyline points="8 6 2 12 8 18"/>
                </svg>
            );

            const Trophy = () => (
                <svg className="icon text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
                    <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
                    <path d="M4 22h16"/>
                    <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
                    <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
                    <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
                </svg>
            );

            const Lightbulb = () => (
                <svg className="icon text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>
                    <path d="M9 18h6"/>
                    <path d="M10 22h4"/>
                </svg>
            );

            const ChevronRight = () => (
                <svg className="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="9 18 15 12 9 6"/>
                </svg>
            );
            
            const Quiz = () => {
                const [currentStep, setCurrentStep] = React.useState(0);
                const [score, setScore] = React.useState(0);
                const [showResults, setShowResults] = React.useState(false);

                const questions = [
                    {
                        title: "La Passion & Motivation",
                        question: "Quel type d'étudiant recherchez-vous ?",
                        options: [
                            {
                                text: "Quelqu'un qui suit simplement le programme",
                                points: 0
                            },
                            {
                                text: "Un passionné qui s'investit au-delà des attentes avec détermination",
                                points: 1,
                                match: "Ma passion se reflète dans mes projets personnels (comme cette app par exemple). Je m'investis toujours à 100% dans ce qui me passionne."
                            }
                        ]
                    },
                    {
                        title: "L'Esprit d'Équipe",
                        question: "Quelle approche privilégiez-vous pour les projets collaboratifs ?",
                        options: [
                            {
                                text: "Une approche individualiste",
                                points: 0
                            },
                            {
                                text: "Une forte capacité à travailler en équipe et à tirer les autres vers le haut",
                                points: 1,
                                match: "Mon expérience de plongeur scaphandrier m'a appris l'importance du travail d'équipe. Cette compétence, combinée à ma passion pour le partage de connaissances, fait de moi un excellent coéquipier."
                            }
                        ]
                    },
                    {
                        title: "L'Engagement",
                        question: "Quel niveau d'investissement attendez-vous ?",
                        options: [
                            {
                                text: "Se contenter du minimum requis",
                                points: 0
                            },
                            {
                                text: "Un investissement total dans les projets",
                                points: 1,
                                match: "Je ne compte pas mes heures quand il s'agit d'apprendre et de progresser. Que ce soit dans les études ou dans mes projets personnels, je donne toujours le meilleur de moi-même."
                            }
                        ]
                    },
                    {
                        title: "L'Initiative",
                        question: "Quelle attitude privilégiez-vous face aux défis ?",
                        options: [
                            {
                                text: "Attendre les consignes",
                                points: 0
                            },
                            {
                                text: "Prendre des initiatives et chercher des solutions",
                                points: 1,
                                match: "Ma reconversion démontre ma capacité à prendre des initiatives. Je n'hésite pas à me lancer dans des projets ambitieux, comme l'apprentissage autodidacte de la programmation ou la création de nouvelles choses."
                            }
                        ]
                    },
                    {
                        title: "L'Excellence",
                        question: "Quelle approche de l'apprentissage recherchez-vous ?",
                        options: [
                            {
                                text: "Viser la moyenne",
                                points: 0
                            },
                            {
                                text: "Viser l'excellence et le dépassement de soi",
                                points: 1,
                                match: "Que ce soit dans le milieu professionnel, dans mes projets personnels ou dans le sport je vise toujours l'excellence. Mon objectif est de toujours m'améliorer et de repousser mes limites."
                            }
                        ]
                    }
                ];

                const handleAnswer = (points) => {
                    setScore(score + points);
                    if (currentStep < questions.length - 1) {
                        setCurrentStep(currentStep + 1);
                    } else {
                        setShowResults(true);
                    }
                };

                if (showResults) {
                    return <MatchProfile score={score} questions={questions} />;
                }

                return (
                    <div className="w-full bg-slate-900 card">
                        <div className="card-header">
                            <h2 className="text-xl text-white">Trouvez le profil idéal</h2>
                        </div>
                        <div className="space-y-6">
                            <div className="flex items-center gap-2 text-sm text-slate-300">
                                <span>Question {currentStep + 1}/{questions.length}</span>
                                <div className="flex-1 h-1 bg-slate-700 rounded-full">
                                    <div 
                                        className="h-1 bg-blue-500 rounded-full transition-all"
                                        style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
                                    />
                                </div>
                            </div>

                            <div className="p-6 bg-slate-800 rounded-lg">
                                <h3 className="text-lg font-semibold mb-3 text-white">
                                    {questions[currentStep].title}
                                </h3>
                                <p className="text-slate-200 mb-6">
                                    {questions[currentStep].question}
                                </p>
                                
                                <div className="space-y-3">
                                    {questions[currentStep].options.map((option, index) => (
                                        <button
                                            key={index}
                                            className="button"
                                            onClick={() => handleAnswer(option.points)}
                                        >
                                            <ChevronRight />
                                            <span>{option.text}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const MatchProfile = ({ score, questions }) => {
                const matches = questions.filter((q, i) => score > i).map(q => q.options[1].match);
                const icons = [Star, Brain, Code, Trophy, Lightbulb];
                
                const percentage = (score / questions.length) * 100;
                const getMessage = () => {
                    if (percentage === 100) {
                        return "✨ Perfect Match ! Voici pourquoi je suis le candidat idéal";
                    } else if (percentage >= 80) {
                        return "🎯 Excellent ! Découvrez comment je corresponds à vos attentes";
                    } else {
                        return "Voici comment je peux répondre à vos critères";
                    }
                };
                
                return (
                    <div className="w-full bg-black card">
                        <div className="card-header flex items-center gap-3">
                            <Trophy />
                            <h2 className="text-xl text-white">{getMessage()}</h2>
                        </div>
                        <div className="p-4 bg-slate-800 rounded-lg">
                            <div className="results-container space-y-3">
                                {matches.map((match, index) => (
                                    <div key={index} className="p-3 bg-slate-700 rounded-lg flex gap-3 hover:bg-slate-600 transition-all">
                                        {React.createElement(icons[index % icons.length])}
                                        <p className="text-slate-200 flex-1">{match}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            };

            ReactDOM.render(<Quiz />, document.getElementById('quiz-root'));
        </script>
    </body>
    </html>
    """
    
    components.html(quiz_html, height=1000, width=None, scrolling=False)  # Augmenté de 858 à 1000 pixels
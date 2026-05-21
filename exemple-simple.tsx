import React, { useState } from 'react';
import { MessageSquare, Brain, Target, Zap } from 'lucide-react';

const SimpleAIAgent = () => {
  const [userInput, setUserInput] = useState('');
  const [conversation, setConversation] = useState([]);
  const [agentState, setAgentState] = useState({
    perception: '',
    decision: '',
    action: '',
    memory: []
  });

  // COMPOSANTS D'UN AGENT IA
  
  // 1. PERCEPTION - L'agent perçoit son environnement
  const perceive = (input) => {
    const perception = {
      text: input.toLowerCase(),
      timestamp: new Date().toLocaleTimeString(),
      sentiment: analyzeSentiment(input)
    };
    
    setAgentState(prev => ({ ...prev, perception: JSON.stringify(perception, null, 2) }));
    return perception;
  };

  // Analyse simple du sentiment
  const analyzeSentiment = (text) => {
    const positiveWords = ['merci', 'génial', 'super', 'excellent', 'bonjour', 'content'];
    const negativeWords = ['problème', 'bug', 'erreur', 'mauvais', 'aide'];
    
    const lower = text.toLowerCase();
    if (positiveWords.some(word => lower.includes(word))) return 'positif';
    if (negativeWords.some(word => lower.includes(word))) return 'négatif';
    return 'neutre';
  };

  // 2. DÉCISION - L'agent décide quoi faire
  const decide = (perception) => {
    let decision = { intent: '', confidence: 0 };

    // Reconnaissance d'intentions simples
    if (perception.text.includes('météo')) {
      decision = { intent: 'donner_meteo', confidence: 0.9 };
    } else if (perception.text.includes('heure')) {
      decision = { intent: 'donner_heure', confidence: 0.95 };
    } else if (perception.text.includes('calcul') || perception.text.includes('calculer')) {
      decision = { intent: 'faire_calcul', confidence: 0.85 };
    } else if (perception.text.includes('blague') || perception.text.includes('humour')) {
      decision = { intent: 'raconter_blague', confidence: 0.8 };
    } else if (perception.sentiment === 'positif') {
      decision = { intent: 'repondre_positivement', confidence: 0.7 };
    } else {
      decision = { intent: 'conversation_generale', confidence: 0.6 };
    }

    setAgentState(prev => ({ ...prev, decision: JSON.stringify(decision, null, 2) }));
    return decision;
  };

  // 3. ACTION - L'agent exécute une action
  const act = (decision, perception) => {
    let response = '';

    switch (decision.intent) {
      case 'donner_meteo':
        response = "☀️ Il fait beau aujourd'hui ! Température : 22°C";
        break;
      case 'donner_heure':
        response = `⏰ Il est ${new Date().toLocaleTimeString()}`;
        break;
      case 'faire_calcul':
        const numbers = perception.text.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
          const result = parseInt(numbers[0]) + parseInt(numbers[1]);
          response = `🔢 ${numbers[0]} + ${numbers[1]} = ${result}`;
        } else {
          response = "Je peux faire des additions ! Essayez : 'calcule 5 + 3'";
        }
        break;
      case 'raconter_blague':
        response = "😄 Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau !";
        break;
      case 'repondre_positivement':
        response = "😊 Merci ! Je suis ravi de pouvoir vous aider !";
        break;
      default:
        response = "💬 Je suis un agent IA simple. Je peux vous donner l'heure, la météo, faire des calculs, ou raconter une blague !";
    }

    setAgentState(prev => ({ ...prev, action: response }));
    return response;
  };

  // 4. MÉMOIRE - L'agent se souvient des interactions
  const updateMemory = (perception, decision, action) => {
    const memoryEntry = {
      input: perception.text,
      intent: decision.intent,
      output: action,
      time: perception.timestamp
    };

    setAgentState(prev => ({
      ...prev,
      memory: [...prev.memory.slice(-4), memoryEntry] // Garde les 5 dernières interactions
    }));
  };

  // BOUCLE PRINCIPALE DE L'AGENT
  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!userInput.trim()) return;

    // Ajoute le message de l'utilisateur
    setConversation(prev => [...prev, { type: 'user', text: userInput }]);

    // CYCLE PERCEPTION → DÉCISION → ACTION
    const perception = perceive(userInput);
    const decision = decide(perception);
    const action = act(decision, perception);
    updateMemory(perception, decision, action);

    // Ajoute la réponse de l'agent
    setConversation(prev => [...prev, { type: 'agent', text: action }]);
    setUserInput('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <Brain className="w-8 h-8" />
              Agent IA Simple - Démonstration Pédagogique
            </h1>
            <p className="mt-2 text-blue-100">
              Comprendre le fonctionnement d'un agent intelligent : Perception → Décision → Action
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 p-6">
            {/* Zone de conversation */}
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto border-2 border-gray-200">
                <h2 className="font-bold text-lg mb-4 flex items-center gap-2">
                  <MessageSquare className="w-5 h-5" />
                  Conversation
                </h2>
                {conversation.length === 0 ? (
                  <p className="text-gray-400 italic">
                    Commencez une conversation avec l'agent...
                  </p>
                ) : (
                  conversation.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`mb-3 p-3 rounded-lg ${
                        msg.type === 'user'
                          ? 'bg-blue-100 ml-8'
                          : 'bg-green-100 mr-8'
                      }`}
                    >
                      <p className="font-semibold text-xs mb-1">
                        {msg.type === 'user' ? '👤 Vous' : '🤖 Agent'}
                      </p>
                      <p>{msg.text}</p>
                    </div>
                  ))
                )}
              </div>

              {/* Zone d'entrée */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
                  placeholder="Posez une question à l'agent..."
                  className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={handleSubmit}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Envoyer
                </button>
              </div>

              {/* Exemples */}
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="font-semibold mb-2">💡 Essayez ces commandes :</p>
                <div className="flex flex-wrap gap-2">
                  {['Quelle heure est-il ?', 'Météo', 'Calcule 15 + 27', 'Raconte une blague'].map(cmd => (
                    <button
                      key={cmd}
                      onClick={() => setUserInput(cmd)}
                      className="text-sm px-3 py-1 bg-white border border-yellow-300 rounded-full hover:bg-yellow-100"
                    >
                      {cmd}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* État interne de l'agent */}
            <div className="space-y-4">
              <div className="bg-purple-50 rounded-lg p-4 border-2 border-purple-200">
                <h3 className="font-bold flex items-center gap-2 mb-2">
                  <Target className="w-5 h-5 text-purple-600" />
                  1. Perception (Entrée)
                </h3>
                <pre className="text-xs bg-white p-2 rounded overflow-x-auto">
                  {agentState.perception || 'En attente...'}
                </pre>
              </div>

              <div className="bg-orange-50 rounded-lg p-4 border-2 border-orange-200">
                <h3 className="font-bold flex items-center gap-2 mb-2">
                  <Brain className="w-5 h-5 text-orange-600" />
                  2. Décision (Raisonnement)
                </h3>
                <pre className="text-xs bg-white p-2 rounded overflow-x-auto">
                  {agentState.decision || 'En attente...'}
                </pre>
              </div>

              <div className="bg-green-50 rounded-lg p-4 border-2 border-green-200">
                <h3 className="font-bold flex items-center gap-2 mb-2">
                  <Zap className="w-5 h-5 text-green-600" />
                  3. Action (Sortie)
                </h3>
                <p className="text-sm bg-white p-2 rounded">
                  {agentState.action || 'En attente...'}
                </p>
              </div>

              <div className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
                <h3 className="font-bold mb-2">💾 Mémoire (Historique)</h3>
                <div className="text-xs bg-white p-2 rounded max-h-32 overflow-y-auto">
                  {agentState.memory.length === 0 ? (
                    <p className="text-gray-400">Aucune interaction</p>
                  ) : (
                    agentState.memory.map((entry, idx) => (
                      <div key={idx} className="mb-2 pb-2 border-b last:border-0">
                        <p><strong>Entrée:</strong> {entry.input}</p>
                        <p><strong>Intent:</strong> {entry.intent}</p>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Explication pédagogique */}
          <div className="bg-gray-50 border-t-2 border-gray-200 p-6">
            <h2 className="text-xl font-bold mb-4">📚 Qu'est-ce qu'un Agent IA ?</h2>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-bold text-purple-600 mb-2">🎯 Perception</h3>
                <p>L'agent observe son environnement via des capteurs (ici : votre texte). Il analyse et comprend l'entrée.</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-bold text-orange-600 mb-2">🧠 Décision</h3>
                <p>L'agent raisonne et choisit quelle action entreprendre selon son objectif et ses connaissances.</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-bold text-green-600 mb-2">⚡ Action</h3>
                <p>L'agent exécute une action qui modifie son environnement (ici : une réponse textuelle).</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleAIAgent;
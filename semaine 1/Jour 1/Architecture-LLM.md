# 🧠 Semaine 1 – Jour 1 : Architecture des LLM (Transformers)

## Objectif du jour
Comprendre les **composantes fondamentales** d’un modèle de langage de type **Transformer**, base des LLM modernes comme GPT, BERT ou LLaMA.

---

## ⚙️ Architecture générale d’un Transformer

Un **Transformer** est un modèle de deep learning introduit par Vaswani et al. (2017) dans *“Attention Is All You Need”*.  
Il repose sur trois concepts clés :

### 1. **Embeddings**
- Représentation vectorielle d’un mot, token ou sous-token.  
- Convertit le texte en nombres manipulables par le modèle.  
- Types : **Word embeddings**, **Positional embeddings** (position des mots dans la phrase).

### 2. **Self-Attention**
- Mécanisme central permettant au modèle de “pondérer” l’importance des mots entre eux dans une phrase.  
- Calcule pour chaque mot une **relation pondérée** avec les autres.  
- Trois vecteurs sont appris :
  - **Query (Q)** : ce que le mot cherche à comprendre  
  - **Key (K)** : ce que le mot représente  
  - **Value (V)** : l’information transportée  

> 🧩 Formule clé :  
> `Attention(Q, K, V) = softmax((Q·Kᵀ) / √dₖ) · V`

### 3. **Multi-Head Attention**
- Le modèle apprend **plusieurs types de relations** en parallèle.  
- Chaque “head” capture une dimension différente du sens (grammaire, contexte, dépendances…).
- Les têtes sont ensuite **concaténées et réintégrées** dans le modèle.

---

## 🧱 Structure d’un bloc Transformer
Un bloc standard comprend :
1. **Multi-Head Self-Attention**
2. **Add & Norm (résidus + normalisation)**
3. **Feed Forward Network (FFN)**
4. **Add & Norm**

Ces blocs sont empilés en profondeur (12, 24, 70+ couches selon la taille du modèle).

---

## 📘 Pour aller plus loin (sources gratuites)
- 🔗 [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)
- 🎓 [Harvard CS50: Introduction to Transformers](https://youtu.be/kCc8FmEb1nY)
- 📄 [Paper original : Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## 💡 Notes du formateur
> Les embeddings traduisent les mots en nombres,  
> l’attention apprend **où regarder**,  
> les multi-heads permettent **plusieurs perspectives** simultanées.  
> C’est cette architecture qui permet aux LLM de comprendre le contexte global d’une phrase.

---

### 🧪 À tester
👉 Ouvre le notebook `S1_J1_Transformers_Intro.ipynb` pour visualiser l’attention sur une phrase simple.

# Copyright (c) 2025 Shimon Nawaz Loan. All rights reserved.
#
# This software, including all associated code, documentation, and data (collectively, the "Software"),
# is the exclusive property of Shimon Nawaz Loan. Unauthorized copying, modification, distribution,
# or use of this Software, in whole or in part, is strictly prohibited without prior written permission
# from Shimon Nawaz Loan, except as expressly permitted under the End User License Agreement (EULA) below.
#
# END USER LICENSE AGREEMENT (EULA)
#
# This End User License Agreement ("Agreement") governs the use of the MBTI Personality Bot software
# ("Software") created by Shimon Nawaz Loan. By using the Software, you ("User") agree to be bound by
# the terms of this Agreement.
#
# 1. License Grant
#    Shimon Nawaz Loan grants the User a non-exclusive, non-transferable, revocable license to use the
#    Software for personal, non-commercial purposes, subject to the terms of this Agreement.
#
# 2. Restrictions
#    The User shall not:
#    - Copy, modify, or create derivative works of the Software.
#    - Distribute, sell, sublicense, or transfer the Software to any third party.
#    - Reverse engineer, decompile, or disassemble the Software.
#    - Use the Software for any commercial purpose without prior written consent from Shimon Nawaz Loan.
#
# 3. Ownership
#    The Software, including all intellectual property rights, is owned by Shimon Nawaz Loan. The User
#    acknowledges that no title or ownership of the Software is transferred under this Agreement.
#
# 4. No Warranty
#    The Software is provided "as is" without any warranties, express or implied, including but not limited
#    to warranties of merchantability, fitness for a particular purpose, or non-infringement. Shimon Nawaz
#    Loan does not guarantee the accuracy, reliability, or availability of the Software.
#
# 5. Limitation of Liability
#    Shimon Nawaz Loan shall not be liable for any direct, indirect, incidental, special, or consequential
#    damages arising from the use or inability to use the Software, even if advised of the possibility of
#    such damages.
#
# 6. Termination
#    This Agreement is effective until terminated. Shimon Nawaz Loan may terminate this Agreement at any
#    time if the User breaches its terms. Upon termination, the User must cease all use of the Software.
#
# 7. Governing Law
#    This Agreement shall be governed by and construed in accordance with the laws of the jurisdiction in
#    which Shimon Nawaz Loan resides, without regard to its conflict of law principles.
#
# 8. Contact
#    For inquiries regarding this Agreement or the Software, contact Shimon Nawaz Loan at [insert contact
#    information, e.g., email address].
#
# By using the Software, the User acknowledges that they have read, understood, and agreed to be bound by
# the terms of this Agreement.
#

import pandas as pd
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
import logging

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for ConversationHandler
GENDER, EI, SN, TF, JP = range(5)

# Embedded MBTI data (replacing CSV)
mbti_data = [
    {
        "PersonalityType": "ISTJ", "Gender": "Male",
        "Description": "Quiet, serious, reliable, and logical. ISTJs value tradition, loyalty, and structure, working steadily toward goals with a focus on facts and details.",
        "FamousPerson1": "King George III", "FamousPerson2": "Charlemagne", "FamousPerson3": "Louis XIV", "FamousPerson4": "Augustus Caesar", "FamousPerson5": "Frederick the Great",
        "Animal1": "Elephant", "Animal2": "Owl", "Animal3": "Wolf",
        "AnimeCharacter1": "Levi Ackerman", "AnimeCharacter2": "Sung Jinwoo", "AnimeCharacter3": "Daichi Sawamura", "AnimeCharacter4": "Gintoki Sakata", "AnimeCharacter5": "Zoro Roronoa",
        "AnimeSeries1": "Attack on Titan", "AnimeSeries2": "Solo Leveling", "AnimeSeries3": "Haikyuu!!", "AnimeSeries4": "Gintama", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Nick Fury", "MarvelCharacter2": "Tony Stark (ISTJ tendencies in duty)", "MarvelCharacter3": "War Machine",
        "DCCharacter1": "Batman", "DCCharacter2": "Hawkman", "DCCharacter3": "Green Arrow",
        "Occupation1": "Accountant", "Occupation2": "Engineer", "Occupation3": "Logistics Manager",
        "BollywoodActor1": "Akshay Kumar", "BollywoodActor2": "Ajay Devgn", "BollywoodActor3": "Nawazuddin Siddiqui",
        "HollywoodActor1": "Tom Hanks", "HollywoodActor2": "Hugh Jackman", "HollywoodActor3": "Clint Eastwood"
    },
    {
        "PersonalityType": "ISTJ", "Gender": "Female",
        "Description": "Quiet, serious, reliable, and logical. ISTJs value tradition, loyalty, and structure, working steadily toward goals with a focus on facts and details.",
        "FamousPerson1": "Queen Victoria", "FamousPerson2": "Elizabeth I", "FamousPerson3": "Catherine the Great", "FamousPerson4": "Maria Theresa", "FamousPerson5": "Cleopatra",
        "Animal1": "Elephant", "Animal2": "Owl", "Animal3": "Wolf",
        "AnimeCharacter1": "Levi Ackerman", "AnimeCharacter2": "Sung Jinwoo", "AnimeCharacter3": "Daichi Sawamura", "AnimeCharacter4": "Gintoki Sakata", "AnimeCharacter5": "Zoro Roronoa",
        "AnimeSeries1": "Attack on Titan", "AnimeSeries2": "Solo Leveling", "AnimeSeries3": "Haikyuu!!", "AnimeSeries4": "Gintama", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Nick Fury", "MarvelCharacter2": "Tony Stark (ISTJ tendencies in duty)", "MarvelCharacter3": "War Machine",
        "DCCharacter1": "Batman", "DCCharacter2": "Hawkman", "DCCharacter3": "Green Arrow",
        "Occupation1": "Accountant", "Occupation2": "Engineer", "Occupation3": "Logistics Manager",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Anushka Sharma", "BollywoodActor3": "Vidya Balan",
        "HollywoodActor1": "Meryl Streep", "HollywoodActor2": "Angelina Jolie", "HollywoodActor3": "Natalie Portman"
    },
    {
        "PersonalityType": "ISFJ", "Gender": "Male",
        "Description": "Warm-hearted, responsible, and reserved. ISFJs are conscientious, loyal, and focused on creating harmony, often putting others’ needs first.",
        "FamousPerson1": "King Arthur", "FamousPerson2": "Edward VI", "FamousPerson3": "Saint Louis IX", "FamousPerson4": "Alfred the Great", "FamousPerson5": "Philip II of Spain",
        "Animal1": "Dolphin", "Animal2": "Deer", "Animal3": "Labrador Retriever",
        "AnimeCharacter1": "Tanjiro Kamado", "AnimeCharacter2": "Armin Arlert", "AnimeCharacter3": "Yamaguchi Tadashi", "AnimeCharacter4": "Mumen Rider", "AnimeCharacter5": "Izuku Midoriya",
        "AnimeSeries1": "Demon Slayer", "AnimeSeries2": "Attack on Titan", "AnimeSeries3": "Haikyuu!!", "AnimeSeries4": "One Punch Man", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Beast", "MarvelCharacter3": "Colossus",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Flash",
        "Occupation1": "Nurse", "Occupation2": "Teacher", "Occupation3": "Social Worker",
        "BollywoodActor1": "Ranbir Kapoor", "BollywoodActor2": "Shahid Kapoor", "BollywoodActor3": "Varun Dhawan",
        "HollywoodActor1": "Chris Evans", "HollywoodActor2": "Tom Holland", "HollywoodActor3": "Robert Downey Jr."
    },
    {
        "PersonalityType": "ISFJ", "Gender": "Female",
        "Description": "Warm-hearted, responsible, and reserved. ISFJs are conscientious, loyal, and focused on creating harmony, often putting others’ needs first.",
        "FamousPerson1": "Queen Elizabeth II", "FamousPerson2": "Marie Antoinette", "FamousPerson3": "Isabella I of Castile", "FamousPerson4": "Queen Alexandra", "FamousPerson5": "Empress Theodora",
        "Animal1": "Dolphin", "Animal2": "Deer", "Animal3": "Labrador Retriever",
        "AnimeCharacter1": "Tanjiro Kamado", "AnimeCharacter2": "Armin Arlert", "AnimeCharacter3": "Yamaguchi Tadashi", "AnimeCharacter4": "Mumen Rider", "AnimeCharacter5": "Izuku Midoriya",
        "AnimeSeries1": "Demon Slayer", "AnimeSeries2": "Attack on Titan", "AnimeSeries3": "Haikyuu!!", "AnimeSeries4": "One Punch Man", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Beast", "MarvelCharacter3": "Colossus",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Flash",
        "Occupation1": "Nurse", "Occupation2": "Teacher", "Occupation3": "Social Worker",
        "BollywoodActor1": "Priyanka Chopra", "BollywoodActor2": "Kangana Ranaut", "BollywoodActor3": "Taapsee Pannu",
        "HollywoodActor1": "Scarlett Johansson", "HollywoodActor2": "Emma Watson", "HollywoodActor3": "Jennifer Lawrence"
    },
    {
        "PersonalityType": "INFJ", "Gender": "Male",
        "Description": "Insightful, idealistic, and reserved. INFJs seek meaning in relationships and ideas, with a strong vision for positive change.",
        "FamousPerson1": "King Ashoka", "FamousPerson2": "Marcus Aurelius", "FamousPerson3": "Akbar the Great", "FamousPerson4": "Henry V", "FamousPerson5": "Saladin",
        "Animal1": "Swan", "Animal2": "Owl", "Animal3": "Dolphin",
        "AnimeCharacter1": "Alphonse Elric", "AnimeCharacter2": "Nagisa Shiota", "AnimeCharacter3": "Yuzuru Otonashi", "AnimeCharacter4": "Mitsuki Bakugo", "AnimeCharacter5": "Itachi Uchiha",
        "AnimeSeries1": "Fullmetal Alchemist", "AnimeSeries2": "Assassination Classroom", "AnimeSeries3": "Angel Beats", "AnimeSeries4": "My Hero Academia", "AnimeSeries5": "Naruto",
        "MarvelCharacter1": "Vision", "MarvelCharacter2": "Professor X", "MarvelCharacter3": "Doctor Strange",
        "DCCharacter1": "Superman", "DCCharacter2": "Green Lantern (John Stewart)", "DCCharacter3": "Martian Manhunter",
        "Occupation1": "Counselor", "Occupation2": "Writer", "Occupation3": "Nonprofit Director",
        "BollywoodActor1": "Aamir Khan", "BollywoodActor2": "Farhan Akhtar", "BollywoodActor3": "Abhishek Bachchan",
        "HollywoodActor1": "Leonardo DiCaprio", "HollywoodActor2": "Christian Bale", "HollywoodActor3": "Johnny Depp"
    },
    {
        "PersonalityType": "INFJ", "Gender": "Female",
        "Description": "Insightful, idealistic, and reserved. INFJs seek meaning in relationships and ideas, with a strong vision for positive change.",
        "FamousPerson1": "Joan of Arc", "FamousPerson2": "Eleanor of Aquitaine", "FamousPerson3": "Hatshepsut", "FamousPerson4": "Empress Wu Zetian", "FamousPerson5": "Boudicca",
        "Animal1": "Swan", "Animal2": "Owl", "Animal3": "Dolphin",
        "AnimeCharacter1": "Alphonse Elric", "AnimeCharacter2": "Nagisa Shiota", "AnimeCharacter3": "Yuzuru Otonashi", "AnimeCharacter4": "Mitsuki Bakugo", "AnimeCharacter5": "Itachi Uchiha",
        "AnimeSeries1": "Fullmetal Alchemist", "AnimeSeries2": "Assassination Classroom", "AnimeSeries3": "Angel Beats", "AnimeSeries4": "My Hero Academia", "AnimeSeries5": "Naruto",
        "MarvelCharacter1": "Vision", "MarvelCharacter2": "Professor X", "MarvelCharacter3": "Doctor Strange",
        "DCCharacter1": "Superman", "DCCharacter2": "Green Lantern (John Stewart)", "DCCharacter3": "Martian Manhunter",
        "Occupation1": "Counselor", "Occupation2": "Writer", "Occupation3": "Nonprofit Director",
        "BollywoodActor1": "Alia Bhatt", "BollywoodActor2": "Shraddha Kapoor", "BollywoodActor3": "Parineeti Chopra",
        "HollywoodActor1": "Nicole Kidman", "HollywoodActor2": "Keira Knightley", "HollywoodActor3": "Cate Blanchett"
    },
    {
        "PersonalityType": "INTJ", "Gender": "Male",
        "Description": "Strategic, independent, and visionary. INTJs are driven by long-term goals, high standards, and a knack for seeing the big picture.",
        "FamousPerson1": "Napoleon Bonaparte", "FamousPerson2": "Hannibal Barca", "FamousPerson3": "Julius Caesar", "FamousPerson4": "Charlemagne", "FamousPerson5": "Elon Musk (modern equivalent)",
        "Animal1": "Eagle", "Animal2": "Owl", "Animal3": "Panther",
        "AnimeCharacter1": "Lelouch Lamperouge", "AnimeCharacter2": "Senku Ishigami", "AnimeCharacter3": "Light Yagami", "AnimeCharacter4": "Shikamaru Nara", "AnimeCharacter5": "Byakuya Kuchiki",
        "AnimeSeries1": "Code Geass", "AnimeSeries2": "Dr. Stone", "AnimeSeries3": "Death Note", "AnimeSeries4": "Naruto", "AnimeSeries5": "Bleach",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Doctor Strange", "MarvelCharacter3": "Loki",
        "DCCharacter1": "Batman", "DCCharacter2": "Lex Luthor", "DCCharacter3": "Ra’s al Ghul",
        "Occupation1": "Scientist", "Occupation2": "Strategist", "Occupation3": "Entrepreneur",
        "BollywoodActor1": "Amitabh Bachchan", "BollywoodActor2": "Hrithik Roshan", "BollywoodActor3": "Saif Ali Khan",
        "HollywoodActor1": "Robert Downey Jr.", "HollywoodActor2": "Benedict Cumberbatch", "HollywoodActor3": "Chris Hemsworth"
    },
    {
        "PersonalityType": "INTJ", "Gender": "Female",
        "Description": "Strategic, independent, and visionary. INTJs are driven by long-term goals, high standards, and a knack for seeing the big picture.",
        "FamousPerson1": "Cleopatra", "FamousPerson2": "Catherine de Medici", "FamousPerson3": "Indira Gandhi", "FamousPerson4": "Empress Dowager Cixi", "FamousPerson5": "Golda Meir",
        "Animal1": "Eagle", "Animal2": "Owl", "Animal3": "Panther",
        "AnimeCharacter1": "Lelouch Lamperouge", "AnimeCharacter2": "Senku Ishigami", "AnimeCharacter3": "Light Yagami", "AnimeCharacter4": "Shikamaru Nara", "AnimeCharacter5": "Byakuya Kuchiki",
        "AnimeSeries1": "Code Geass", "AnimeSeries2": "Dr. Stone", "AnimeSeries3": "Death Note", "AnimeSeries4": "Naruto", "AnimeSeries5": "Bleach",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Doctor Strange", "MarvelCharacter3": "Loki",
        "DCCharacter1": "Batman", "DCCharacter2": "Lex Luthor", "DCCharacter3": "Ra’s al Ghul",
        "Occupation1": "Scientist", "Occupation2": "Strategist", "Occupation3": "Entrepreneur",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Anushka Sharma", "BollywoodActor3": "Vidya Balan",
        "HollywoodActor1": "Meryl Streep", "HollywoodActor2": "Angelina Jolie", "HollywoodActor3": "Natalie Portman"
    },
    {
        "PersonalityType": "ISTP", "Gender": "Male",
        "Description": "Flexible, logical, and action-oriented. ISTPs are hands-on problem-solvers who thrive on understanding how things work.",
        "FamousPerson1": "Genghis Khan", "FamousPerson2": "Alexander the Great", "FamousPerson3": "William the Conqueror", "FamousPerson4": "Richard the Lionheart", "FamousPerson5": "Suleiman the Magnificent",
        "Animal1": "Tiger", "Animal2": "Wolf", "Animal3": "Falcon",
        "AnimeCharacter1": "Kyosuke Munroe", "AnimeCharacter2": "Saitama", "AnimeCharacter3": "Kyojuro Rengoku", "AnimeCharacter4": "Spike Spiegel", "AnimeCharacter5": "Katsuki Bakugo",
        "AnimeSeries1": "My Teen Romantic Comedy Yahari", "AnimeSeries2": "One Punch Man", "AnimeSeries3": "Demon Slayer", "AnimeSeries4": "Cowboy Bebop", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Wolverine", "MarvelCharacter2": "Hawkeye", "MarvelCharacter3": "Winter Soldier",
        "DCCharacter1": "Green Arrow", "DCCharacter2": "Hawkman", "DCCharacter3": "Red Hood",
        "Occupation1": "Mechanic", "Occupation2": "Engineer", "Occupation3": "Pilot",
        "BollywoodActor1": "Ranveer Singh", "BollywoodActor2": "John Abraham", "BollywoodActor3": "Tiger Shroff",
        "HollywoodActor1": "Chris Pratt", "HollywoodActor2": "Tom Hardy", "HollywoodActor3": "Brad Pitt"
    },
    {
        "PersonalityType": "ISTP", "Gender": "Female",
        "Description": "Flexible, logical, and action-oriented. ISTPs are hands-on problem-solvers who thrive on understanding how things work.",
        "FamousPerson1": "Boudicca", "FamousPerson2": "Zenobia", "FamousPerson3": "Matilda of Tuscany", "FamousPerson4": "Isabella of France", "FamousPerson5": "Lakshmibai",
        "Animal1": "Tiger", "Animal2": "Wolf", "Animal3": "Falcon",
        "AnimeCharacter1": "Kyosuke Munroe", "AnimeCharacter2": "Saitama", "AnimeCharacter3": "Kyojuro Rengoku", "AnimeCharacter4": "Spike Spiegel", "AnimeCharacter5": "Katsuki Bakugo",
        "AnimeSeries1": "My Teen Romantic Comedy Yahari", "AnimeSeries2": "One Punch Man", "AnimeSeries3": "Demon Slayer", "AnimeSeries4": "Cowboy Bebop", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Wolverine", "MarvelCharacter2": "Hawkeye", "MarvelCharacter3": "Winter Soldier",
        "DCCharacter1": "Green Arrow", "DCCharacter2": "Hawkman", "DCCharacter3": "Red Hood",
        "Occupation1": "Mechanic", "Occupation2": "Engineer", "Occupation3": "Pilot",
        "BollywoodActor1": "Priyanka Chopra", "BollywoodActor2": "Kangana Ranaut", "BollywoodActor3": "Taapsee Pannu",
        "HollywoodActor1": "Scarlett Johansson", "HollywoodActor2": "Emma Watson", "HollywoodActor3": "Jennifer Lawrence"
    },
    {
        "PersonalityType": "ISFP", "Gender": "Male",
        "Description": "Creative, sensitive, and present-focused. ISFPs value personal freedom, artistic expression, and living in the moment.",
        "FamousPerson1": "King David", "FamousPerson2": "Nero", "FamousPerson3": "Henry VIII", "FamousPerson4": "Edward VIII", "FamousPerson5": "Ludwig II of Bavaria",
        "Animal1": "Deer", "Animal2": "Butterfly", "Animal3": "Cat",
        "AnimeCharacter1": "Zuko", "AnimeCharacter2": "Eren Jaeger", "AnimeCharacter3": "Yuji Itadori", "AnimeCharacter4": "Naruto Uzumaki", "AnimeCharacter5": "Sanji",
        "AnimeSeries1": "Avatar: The Last Airbender", "AnimeSeries2": "Attack on Titan", "AnimeSeries3": "Jujutsu Kaisen", "AnimeSeries4": "Naruto", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Peter Parker", "MarvelCharacter2": "Human Torch", "MarvelCharacter3": "Deadpool",
        "DCCharacter1": "Huntress", "DCCharacter2": "Black Canary", "DCCharacter3": "Beast Boy",
        "Occupation1": "Artist", "Occupation2": "Musician", "Occupation3": "Chef",
        "BollywoodActor1": "Shah Rukh Khan", "BollywoodActor2": "Salman Khan", "BollywoodActor3": "Varun Dhawan",
        "HollywoodActor1": "Johnny Depp", "HollywoodActor2": "Robert Downey Jr.", "HollywoodActor3": "Chris Hemsworth"
    },
    {
        "PersonalityType": "ISFP", "Gender": "Female",
        "Description": "Creative, sensitive, and present-focused. ISFPs value personal freedom, artistic expression, and living in the moment.",
        "FamousPerson1": "Nefertiti", "FamousPerson2": "Anne Boleyn", "FamousPerson3": "Mary Queen of Scots", "FamousPerson4": "Empress Josephine", "FamousPerson5": "Princess Diana",
        "Animal1": "Deer", "Animal2": "Butterfly", "Animal3": "Cat",
        "AnimeCharacter1": "Zuko", "AnimeCharacter2": "Eren Jaeger", "AnimeCharacter3": "Yuji Itadori", "AnimeCharacter4": "Naruto Uzumaki", "AnimeCharacter5": "Sanji",
        "AnimeSeries1": "Avatar: The Last Airbender", "AnimeSeries2": "Attack on Titan", "AnimeSeries3": "Jujutsu Kaisen", "AnimeSeries4": "Naruto", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Peter Parker", "MarvelCharacter2": "Human Torch", "MarvelCharacter3": "Deadpool",
        "DCCharacter1": "Huntress", "DCCharacter2": "Black Canary", "DCCharacter3": "Beast Boy",
        "Occupation1": "Artist", "Occupation2": "Musician", "Occupation3": "Chef",
        "BollywoodActor1": "Katrina Kaif", "BollywoodActor2": "Shraddha Kapoor", "BollywoodActor3": "Alia Bhatt",
        "HollywoodActor1": "Keira Knightley", "HollywoodActor2": "Natalie Portman", "HollywoodActor3": "Scarlett Johansson"
    },
    {
        "PersonalityType": "INFP", "Gender": "Male",
        "Description": "Idealistic, curious, and empathetic. INFPs seek to align their lives with their values, often pursuing creative or humanitarian goals.",
        "FamousPerson1": "King Solomon", "FamousPerson2": "Henry VI", "FamousPerson3": "Ashoka (later life)", "FamousPerson4": "Louis Philippe I", "FamousPerson5": "Baháʼu'lláh",
        "Animal1": "Dove", "Animal2": "Deer", "Animal3": "Swan",
        "AnimeCharacter1": "Shinji Ikari", "AnimeCharacter2": "Tamaki Suoh", "AnimeCharacter3": "Atsushi Nakajima", "AnimeCharacter4": "Kaneki Ken", "AnimeCharacter5": "Haku",
        "AnimeSeries1": "Neon Genesis Evangelion", "AnimeSeries2": "Ouran High School Host Club", "AnimeSeries3": "Bungou Stray Dogs", "AnimeSeries4": "Tokyo Ghoul", "AnimeSeries5": "Spirited Away",
        "MarvelCharacter1": "Peter Parker", "MarvelCharacter2": "Vision", "MarvelCharacter3": "Beast",
        "DCCharacter1": "Superman", "DCCharacter2": "Starman", "DCCharacter3": "Aquaman",
        "Occupation1": "Writer", "Occupation2": "Artist", "Occupation3": "Counselor",
        "BollywoodActor1": "Aamir Khan", "BollywoodActor2": "Farhan Akhtar", "BollywoodActor3": "Abhishek Bachchan",
        "HollywoodActor1": "Leonardo DiCaprio", "HollywoodActor2": "Christian Bale", "HollywoodActor3": "Johnny Depp"
    },
    {
        "PersonalityType": "INFP", "Gender": "Female",
        "Description": "Idealistic, curious, and empathetic. INFPs seek to align their lives with their values, often pursuing creative or humanitarian goals.",
        "FamousPerson1": "Joan of Arc", "FamousPerson2": "Elizabeth of York", "FamousPerson3": "Isabella of Aragon", "FamousPerson4": "Empress Maria Anna", "FamousPerson5": "Jane Grey",
        "Animal1": "Dove", "Animal2": "Deer", "Animal3": "Swan",
        "AnimeCharacter1": "Shinji Ikari", "AnimeCharacter2": "Tamaki Suoh", "AnimeCharacter3": "Atsushi Nakajima", "AnimeCharacter4": "Kaneki Ken", "AnimeCharacter5": "Haku",
        "AnimeSeries1": "Neon Genesis Evangelion", "AnimeSeries2": "Ouran High School Host Club", "AnimeSeries3": "Bungou Stray Dogs", "AnimeSeries4": "Tokyo Ghoul", "AnimeSeries5": "Spirited Away",
        "MarvelCharacter1": "Peter Parker", "MarvelCharacter2": "Vision", "MarvelCharacter3": "Beast",
        "DCCharacter1": "Superman", "DCCharacter2": "Starman", "DCCharacter3": "Aquaman",
        "Occupation1": "Writer", "Occupation2": "Artist", "Occupation3": "Counselor",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Anushka Sharma", "BollywoodActor3": "Vidya Balan",
        "HollywoodActor1": "Emma Watson", "HollywoodActor2": "Jennifer Lawrence", "HollywoodActor3": "Meryl Streep"
    },
    {
        "PersonalityType": "INTP", "Gender": "Male",
        "Description": "Analytical, logical, and independent. INTPs are theoretical thinkers who enjoy exploring ideas and solving complex problems.",
        "FamousPerson1": "Isaac Newton (modern equivalent)", "FamousPerson2": "René Descartes (modern equivalent)", "FamousPerson3": "Socrates (speculated)", "FamousPerson4": "Galileo Galilei (modern equivalent)", "FamousPerson5": "Immanuel Kant (modern equivalent)",
        "Animal1": "Owl", "Animal2": "Raven", "Animal3": "Cat",
        "AnimeCharacter1": "L", "AnimeCharacter2": "Shikamaru Nara", "AnimeCharacter3": "Frieren", "AnimeCharacter4": "Senku Ishigami", "AnimeCharacter5": "Ginko",
        "AnimeSeries1": "Death Note", "AnimeSeries2": "Naruto", "AnimeSeries3": "Frieren: Beyond Journey’s End", "AnimeSeries4": "Dr. Stone", "AnimeSeries5": "Mushishi",
        "MarvelCharacter1": "Bruce Banner", "MarvelCharacter2": "Tony Stark (INTP tendencies in innovation)", "MarvelCharacter3": "Reed Richards",
        "DCCharacter1": "Mr. Terrific", "DCCharacter2": "The Question", "DCCharacter3": "Brainiac 5",
        "Occupation1": "Scientist", "Occupation2": "Philosopher", "Occupation3": "Software Developer",
        "BollywoodActor1": "Ranbir Kapoor", "BollywoodActor2": "Shahid Kapoor", "BollywoodActor3": "Varun Dhawan",
        "HollywoodActor1": "Tom Hanks", "HollywoodActor2": "Hugh Jackman", "HollywoodActor3": "Chris Evans"
    },
    {
        "PersonalityType": "INTP", "Gender": "Female",
        "Description": "Analytical, logical, and independent. INTPs are theoretical thinkers who enjoy exploring ideas and solving complex problems.",
        "FamousPerson1": "Hypatia", "FamousPerson2": "Ada Lovelace", "FamousPerson3": "Emmy Noether", "FamousPerson4": "Rosalind Franklin", "FamousPerson5": "Hedy Lamarr",
        "Animal1": "Owl", "Animal2": "Raven", "Animal3": "Cat",
        "AnimeCharacter1": "L", "AnimeCharacter2": "Shikamaru Nara", "AnimeCharacter3": "Frieren", "AnimeCharacter4": "Senku Ishigami", "AnimeCharacter5": "Ginko",
        "AnimeSeries1": "Death Note", "AnimeSeries2": "Naruto", "AnimeSeries3": "Frieren: Beyond Journey’s End", "AnimeSeries4": "Dr. Stone", "AnimeSeries5": "Mushishi",
        "MarvelCharacter1": "Bruce Banner", "MarvelCharacter2": "Tony Stark (INTP tendencies in innovation)", "MarvelCharacter3": "Reed Richards",
        "DCCharacter1": "Mr. Terrific", "DCCharacter2": "The Question", "DCCharacter3": "Brainiac 5",
        "Occupation1": "Scientist", "Occupation2": "Philosopher", "Occupation3": "Software Developer",
        "BollywoodActor1": "Priyanka Chopra", "BollywoodActor2": "Kangana Ranaut", "BollywoodActor3": "Taapsee Pannu",
        "HollywoodActor1": "Natalie Portman", "HollywoodActor2": "Scarlett Johansson", "HollywoodActor3": "Emma Watson"
    },
    {
        "PersonalityType": "ESTP", "Gender": "Male",
        "Description": "Energetic, pragmatic, and action-oriented. ESTPs thrive on immediate results, are spontaneous, and excel in dynamic environments.",
        "FamousPerson1": "Henry VIII", "FamousPerson2": "Peter the Great", "FamousPerson3": "Genghis Khan", "FamousPerson4": "Theodore Roosevelt (modern equivalent)", "FamousPerson5": "Otto von Bismarck",
        "Animal1": "Lion", "Animal2": "Cheetah", "Animal3": "Falcon",
        "AnimeCharacter1": "Natsu Dragneel", "AnimeCharacter2": "Kamina", "AnimeCharacter3": "Ichigo Kurosaki", "AnimeCharacter4": "Yusuke Urameshi", "AnimeCharacter5": "Joseph Joestar",
        "AnimeSeries1": "Fairy Tail", "AnimeSeries2": "Gurren Lagann", "AnimeSeries3": "Bleach", "AnimeSeries4": "YuYu Hakusho", "AnimeSeries5": "JoJo’s Bizarre Adventure",
        "MarvelCharacter1": "Star-Lord", "MarvelCharacter2": "Deadpool", "MarvelCharacter3": "Thor",
        "DCCharacter1": "Green Arrow", "DCCharacter2": "Booster Gold", "DCCharacter3": "Plastic Man",
        "Occupation1": "Entrepreneur", "Occupation2": "Sales Manager", "Occupation3": "Paramedic",
        "BollywoodActor1": "Ranveer Singh", "BollywoodActor2": "John Abraham", "BollywoodActor3": "Tiger Shroff",
        "HollywoodActor1": "Chris Pratt", "HollywoodActor2": "Tom Hardy", "HollywoodActor3": "Brad Pitt"
    },
    {
        "PersonalityType": "ESTP", "Gender": "Female",
        "Description": "Energetic, pragmatic, and action-oriented. ESTPs thrive on immediate results, are spontaneous, and excel in dynamic environments.",
        "FamousPerson1": "Cleopatra", "FamousPerson2": "Catherine the Great", "FamousPerson3": "Anne Bonny", "FamousPerson4": "Empress Theodora", "FamousPerson5": "Pirate Queen Zheng Yi Sao",
        "Animal1": "Lion", "Animal2": "Cheetah", "Animal3": "Falcon",
        "AnimeCharacter1": "Natsu Dragneel", "AnimeCharacter2": "Kamina", "AnimeCharacter3": "Ichigo Kurosaki", "AnimeCharacter4": "Yusuke Urameshi", "AnimeCharacter5": "Joseph Joestar",
        "AnimeSeries1": "Fairy Tail", "AnimeSeries2": "Gurren Lagann", "AnimeSeries3": "Bleach", "AnimeSeries4": "YuYu Hakusho", "AnimeSeries5": "JoJo’s Bizarre Adventure",
        "MarvelCharacter1": "Star-Lord", "MarvelCharacter2": "Deadpool", "MarvelCharacter3": "Thor",
        "DCCharacter1": "Green Arrow", "DCCharacter2": "Booster Gold", "DCCharacter3": "Plastic Man",
        "Occupation1": "Entrepreneur", "Occupation2": "Sales Manager", "Occupation3": "Paramedic",
        "BollywoodActor1": "Katrina Kaif", "BollywoodActor2": "Shraddha Kapoor", "BollywoodActor3": "Alia Bhatt",
        "HollywoodActor1": "Scarlett Johansson", "HollywoodActor2": "Angelina Jolie", "HollywoodActor3": "Jennifer Lawrence"
    },
    {
        "PersonalityType": "ESFP", "Gender": "Male",
        "Description": "Outgoing, spontaneous, and fun-loving. ESFPs live in the moment, bringing energy and enthusiasm to their work and relationships.",
        "FamousPerson1": "King Louis XV", "FamousPerson2": "Edward VII", "FamousPerson3": "Henry III of France", "FamousPerson4": "George IV", "FamousPerson5": "Caligula",
        "Animal1": "Peacock", "Animal2": "Dolphin", "Animal3": "Parrot",
        "AnimeCharacter1": "Luffy Monkey D.", "AnimeCharacter2": "Usopp", "AnimeCharacter3": "Konohamaru Sarutobi", "AnimeCharacter4": "Gintoki Sakata", "AnimeCharacter5": "Denji",
        "AnimeSeries1": "One Piece", "AnimeSeries2": "One Piece", "AnimeSeries3": "Naruto", "AnimeSeries4": "Gintama", "AnimeSeries5": "Chainsaw Man",
        "MarvelCharacter1": "Human Torch", "MarvelCharacter2": "Star-Lord", "MarvelCharacter3": "Spider-Man",
        "DCCharacter1": "Beast Boy", "DCCharacter2": "Plastic Man", "DCCharacter3": "Blue Beetle",
        "Occupation1": "Performer", "Occupation2": "Event Planner", "Occupation3": "Marketing Specialist",
        "BollywoodActor1": "Salman Khan", "BollywoodActor2": "Varun Dhawan", "BollywoodActor3": "Ranbir Kapoor",
        "HollywoodActor1": "Chris Hemsworth", "HollywoodActor2": "Will Smith", "HollywoodActor3": "Johnny Depp"
    },
    {
        "PersonalityType": "ESFP", "Gender": "Female",
        "Description": "Outgoing, spontaneous, and fun-loving. ESFPs live in the moment, bringing energy and enthusiasm to their work and relationships.",
        "FamousPerson1": "Marie Antoinette", "FamousPerson2": "Empress Josephine", "FamousPerson3": "Messalina", "FamousPerson4": "Queen Alexandra", "FamousPerson5": "Isabella of France",
        "Animal1": "Peacock", "Animal2": "Dolphin", "Animal3": "Parrot",
        "AnimeCharacter1": "Luffy Monkey D.", "AnimeCharacter2": "Usopp", "AnimeCharacter3": "Konohamaru Sarutobi", "AnimeCharacter4": "Gintoki Sakata", "AnimeCharacter5": "Denji",
        "AnimeSeries1": "One Piece", "AnimeSeries2": "One Piece", "AnimeSeries3": "Naruto", "AnimeSeries4": "Gintama", "AnimeSeries5": "Chainsaw Man",
        "MarvelCharacter1": "Human Torch", "MarvelCharacter2": "Star-Lord", "MarvelCharacter3": "Spider-Man",
        "DCCharacter1": "Beast Boy", "DCCharacter2": "Plastic Man", "DCCharacter3": "Blue Beetle",
        "Occupation1": "Performer", "Occupation2": "Event Planner", "Occupation3": "Marketing Specialist",
        "BollywoodActor1": "Katrina Kaif", "BollywoodActor2": "Deepika Padukone", "BollywoodActor3": "Alia Bhatt",
        "HollywoodActor1": "Margot Robbie", "HollywoodActor2": "Scarlett Johansson", "HollywoodActor3": "Emma Stone"
    },
    {
        "PersonalityType": "ENFP", "Gender": "Male",
        "Description": "Enthusiastic, creative, and sociable. ENFPs are imaginative, driven by possibilities, and inspire others with their energy.",
        "FamousPerson1": "King Richard I", "FamousPerson2": "Edward VIII", "FamousPerson3": "Louis Philippe I", "FamousPerson4": "Victor Emmanuel II", "FamousPerson5": "Ferdinand I of Austria",
        "Animal1": "Parrot", "Animal2": "Butterfly", "Animal3": "Dolphin",
        "AnimeCharacter1": "Naruto Uzumaki", "AnimeCharacter2": "Aang", "AnimeCharacter3": "Tamaki Suoh", "AnimeCharacter4": "Izuku Midoriya", "AnimeCharacter5": "Luffy Monkey D.",
        "AnimeSeries1": "Naruto", "AnimeSeries2": "Avatar: The Last Airbender", "AnimeSeries3": "Ouran High School Host Club", "AnimeSeries4": "My Hero Academia", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Star-Lord", "MarvelCharacter2": "Spider-Man", "MarvelCharacter3": "Human Torch",
        "DCCharacter1": "Beast Boy", "DCCharacter2": "Blue Beetle", "DCCharacter3": "Plastic Man",
        "Occupation1": "Teacher", "Occupation2": "Writer", "Occupation3": "Marketing Manager",
        "BollywoodActor1": "Shah Rukh Khan", "BollywoodActor2": "Ranveer Singh", "BollywoodActor3": "Varun Dhawan",
        "HollywoodActor1": "Robert Downey Jr.", "HollywoodActor2": "Chris Pratt", "HollywoodActor3": "Will Smith"
    },
    {
        "PersonalityType": "ENFP", "Gender": "Female",
        "Description": "Enthusiastic, creative, and sociable. ENFPs are imaginative, driven by possibilities, and inspire others with their energy.",
        "FamousPerson1": "Elizabeth I", "FamousPerson2": "Anne of Cleves", "FamousPerson3": "Maria Theresa", "FamousPerson4": "Queen Christina", "FamousPerson5": "Catherine of Aragon",
        "Animal1": "Parrot", "Animal2": "Butterfly", "Animal3": "Dolphin",
        "AnimeCharacter1": "Naruto Uzumaki", "AnimeCharacter2": "Aang", "AnimeCharacter3": "Tamaki Suoh", "AnimeCharacter4": "Izuku Midoriya", "AnimeCharacter5": "Luffy Monkey D.",
        "AnimeSeries1": "Naruto", "AnimeSeries2": "Avatar: The Last Airbender", "AnimeSeries3": "Ouran High School Host Club", "AnimeSeries4": "My Hero Academia", "AnimeSeries5": "One Piece",
        "MarvelCharacter1": "Star-Lord", "MarvelCharacter2": "Spider-Man", "MarvelCharacter3": "Human Torch",
        "DCCharacter1": "Beast Boy", "DCCharacter2": "Blue Beetle", "DCCharacter3": "Plastic Man",
        "Occupation1": "Teacher", "Occupation2": "Writer", "Occupation3": "Marketing Manager",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Priyanka Chopra", "BollywoodActor3": "Anushka Sharma",
        "HollywoodActor1": "Emma Stone", "HollywoodActor2": "Jennifer Lawrence", "HollywoodActor3": "Margot Robbie"
    },
    {
        "PersonalityType": "ENFJ", "Gender": "Male",
        "Description": "Charismatic, empathetic, and inspiring. ENFJs are natural leaders who focus on helping others and fostering harmony.",
        "FamousPerson1": "Martin Luther King Jr. (modern equivalent)", "FamousPerson2": "Charlemagne", "FamousPerson3": "Henry V", "FamousPerson4": "Akbar the Great", "FamousPerson5": "Alfred the Great",
        "Animal1": "Dolphin", "Animal2": "Lion", "Animal3": "Elephant",
        "AnimeCharacter1": "Tanjiro Kamado", "AnimeCharacter2": "Daichi Sawamura", "AnimeCharacter3": "All Might", "AnimeCharacter4": "Jonathan Joestar", "AnimeCharacter5": "Soma Yukihira",
        "AnimeSeries1": "Demon Slayer", "AnimeSeries2": "Haikyuu!!", "AnimeSeries3": "My Hero Academia", "AnimeSeries4": "JoJo’s Bizarre Adventure", "AnimeSeries5": "Food Wars",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Professor X", "MarvelCharacter3": "Vision",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Green Lantern (Hal Jordan)",
        "Occupation1": "Teacher", "Occupation2": "Counselor", "Occupation3": "Nonprofit Director",
        "BollywoodActor1": "Aamir Khan", "BollywoodActor2": "Akshay Kumar", "BollywoodActor3": "Shahid Kapoor",
        "HollywoodActor1": "Chris Evans", "HollywoodActor2": "Leonardo DiCaprio", "HollywoodActor3": "Tom Hanks"
    },
    {
        "PersonalityType": "ENFJ", "Gender": "Female",
        "Description": "Charismatic, empathetic, and inspiring. ENFJs are natural leaders who focus on helping others and fostering harmony.",
        "FamousPerson1": "Eleanor of Aquitaine", "FamousPerson2": "Queen Victoria", "FamousPerson3": "Isabella I of Castile", "FamousPerson4": "Empress Maria Theresa", "FamousPerson5": "Joan of Arc",
        "Animal1": "Dolphin", "Animal2": "Lion", "Animal3": "Elephant",
        "AnimeCharacter1": "Tanjiro Kamado", "AnimeCharacter2": "Daichi Sawamura", "AnimeCharacter3": "All Might", "AnimeCharacter4": "Jonathan Joestar", "AnimeCharacter5": "Soma Yukihira",
        "AnimeSeries1": "Demon Slayer", "AnimeSeries2": "Haikyuu!!", "AnimeSeries3": "My Hero Academia", "AnimeSeries4": "JoJo’s Bizarre Adventure", "AnimeSeries5": "Food Wars",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Professor X", "MarvelCharacter3": "Vision",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Green Lantern (Hal Jordan)",
        "Occupation1": "Teacher", "Occupation2": "Counselor", "Occupation3": "Nonprofit Director",
        "BollywoodActor1": "Alia Bhatt", "BollywoodActor2": "Kangana Ranaut", "BollywoodActor3": "Taapsee Pannu",
        "HollywoodActor1": "Meryl Streep", "HollywoodActor2": "Natalie Portman", "HollywoodActor3": "Emma Watson"
    },
    {
        "PersonalityType": "ENTJ", "Gender": "Male",
        "Description": "Confident, strategic, and goal-oriented. ENTJs are natural leaders who excel at organizing and driving ambitious projects.",
        "FamousPerson1": "Julius Caesar", "FamousPerson2": "Napoleon Bonaparte", "FamousPerson3": "Alexander the Great", "FamousPerson4": "Otto von Bismarck", "FamousPerson5": "Winston Churchill (modern equivalent)",
        "Animal1": "Lion", "Animal2": "Eagle", "Animal3": "Shark",
        "AnimeCharacter1": "Senku Ishigami", "AnimeCharacter2": "Lelouch Lamperouge", "AnimeCharacter3": "Escanor", "AnimeCharacter4": "Roy Mustang", "AnimeCharacter5": "Vegeta",
        "AnimeSeries1": "Dr. Stone", "AnimeSeries2": "Code Geass", "AnimeSeries3": "Seven Deadly Sins", "AnimeSeries4": "Fullmetal Alchemist", "AnimeSeries5": "Dragon Ball Z",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Loki", "MarvelCharacter3": "Doctor Doom",
        "DCCharacter1": "Lex Luthor", "DCCharacter2": "Ra’s al Ghul", "DCCharacter3": "Batman",
        "Occupation1": "CEO", "Occupation2": "Politician", "Occupation3": "Entrepreneur",
        "BollywoodActor1": "Amitabh Bachchan", "BollywoodActor2": "Hrithik Roshan", "BollywoodActor3": "Saif Ali Khan",
        "HollywoodActor1": "Robert Downey Jr.", "HollywoodActor2": "Benedict Cumberbatch", "HollywoodActor3": "Chris Hemsworth"
    },
    {
        "PersonalityType": "ENTJ", "Gender": "Female",
        "Description": "Confident, strategic, and goal-oriented. ENTJs are natural leaders who excel at organizing and driving ambitious projects.",
        "FamousPerson1": "Catherine the Great", "FamousPerson2": "Indira Gandhi", "FamousPerson3": "Margaret Thatcher (modern equivalent)", "FamousPerson4": "Cleopatra", "FamousPerson5": "Golda Meir",
        "Animal1": "Lion", "Animal2": "Eagle", "Animal3": "Shark",
        "AnimeCharacter1": "Senku Ishigami", "AnimeCharacter2": "Lelouch Lamperouge", "AnimeCharacter3": "Escanor", "AnimeCharacter4": "Roy Mustang", "AnimeCharacter5": "Vegeta",
        "AnimeSeries1": "Dr. Stone", "AnimeSeries2": "Code Geass", "AnimeSeries3": "Seven Deadly Sins", "AnimeSeries4": "Fullmetal Alchemist", "AnimeSeries5": "Dragon Ball Z",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Loki", "MarvelCharacter3": "Doctor Doom",
        "DCCharacter1": "Lex Luthor", "DCCharacter2": "Ra’s al Ghul", "DCCharacter3": "Batman",
        "Occupation1": "CEO", "Occupation2": "Politician", "Occupation3": "Entrepreneur",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Anushka Sharma", "BollywoodActor3": "Vidya Balan",
        "HollywoodActor1": "Angelina Jolie", "HollywoodActor2": "Meryl Streep", "HollywoodActor3": "Natalie Portman"
    },
    {
        "PersonalityType": "ENTP", "Gender": "Male",
        "Description": "Innovative, outspoken, and curious. ENTPs thrive on debate, exploring possibilities, and challenging the status quo.",
        "FamousPerson1": "Socrates (speculated)", "FamousPerson2": "Benjamin Franklin (modern equivalent)", "FamousPerson3": "Leonardo da Vinci (modern equivalent)", "FamousPerson4": "Thomas Jefferson (modern equivalent)", "FamousPerson5": "Niccolò Machiavelli",
        "Animal1": "Raven", "Animal2": "Fox", "Animal3": "Monkey",
        "AnimeCharacter1": "Hisoka Morow", "AnimeCharacter2": "Tony Tony Chopper", "AnimeCharacter3": "Kon", "AnimeCharacter4": "Izaya Orihara", "AnimeCharacter5": "Okabe Rintarou",
        "AnimeSeries1": "Hunter x Hunter", "AnimeSeries2": "One Piece", "AnimeSeries3": "Bleach", "AnimeSeries4": "Durarara!!", "AnimeSeries5": "Steins;Gate",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Loki", "MarvelCharacter3": "Deadpool",
        "DCCharacter1": "The Joker", "DCCharacter2": "Booster Gold", "DCCharacter3": "Plastic Man",
        "Occupation1": "Inventor", "Occupation2": "Entrepreneur", "Occupation3": "Lawyer",
        "BollywoodActor1": "Ranbir Kapoor", "BollywoodActor2": "Shahid Kapoor", "BollywoodActor3": "Varun Dhawan",
        "HollywoodActor1": "Johnny Depp", "HollywoodActor2": "Robert Downey Jr.", "HollywoodActor3": "Chris Pratt"
    },
    {
        "PersonalityType": "ENTP", "Gender": "Female",
        "Description": "Innovative, outspoken, and curious. ENTPs thrive on debate, exploring possibilities, and challenging the status quo.",
        "FamousPerson1": "Hypatia", "FamousPerson2": "Catherine de Medici", "FamousPerson3": "Queen Christina", "FamousPerson4": "Ada Lovelace", "FamousPerson5": "Ayn Rand (modern equivalent)",
        "Animal1": "Raven", "Animal2": "Fox", "Animal3": "Monkey",
        "AnimeCharacter1": "Hisoka Morow", "AnimeCharacter2": "Tony Tony Chopper", "AnimeCharacter3": "Kon", "AnimeCharacter4": "Izaya Orihara", "AnimeCharacter5": "Okabe Rintarou",
        "AnimeSeries1": "Hunter x Hunter", "AnimeSeries2": "One Piece", "AnimeSeries3": "Bleach", "AnimeSeries4": "Durarara!!", "AnimeSeries5": "Steins;Gate",
        "MarvelCharacter1": "Tony Stark", "MarvelCharacter2": "Loki", "MarvelCharacter3": "Deadpool",
        "DCCharacter1": "The Joker", "DCCharacter2": "Booster Gold", "DCCharacter3": "Plastic Man",
        "Occupation1": "Inventor", "Occupation2": "Entrepreneur", "Occupation3": "Lawyer",
        "BollywoodActor1": "Priyanka Chopra", "BollywoodActor2": "Kangana Ranaut", "BollywoodActor3": "Taapsee Pannu",
        "HollywoodActor1": "Scarlett Johansson", "HollywoodActor2": "Emma Watson", "HollywoodActor3": "Jennifer Lawrence"
    },
    {
        "PersonalityType": "ESTJ", "Gender": "Male",
        "Description": "Decisive, organized, and results-driven. ESTJs are natural leaders who value efficiency, structure, and clear expectations.",
        "FamousPerson1": "Augustus Caesar", "FamousPerson2": "King David", "FamousPerson3": "Philip II of Spain", "FamousPerson4": "George Washington (modern equivalent)", "FamousPerson5": "Dwight D. Eisenhower (modern equivalent)",
        "Animal1": "Elephant", "Animal2": "Lion", "Animal3": "Bear",
        "AnimeCharacter1": "Tobio Kageyama", "AnimeCharacter2": "Iida Tenya", "AnimeCharacter3": "Roy Mustang", "AnimeCharacter4": "Vegeta", "AnimeCharacter5": "Bakugo Katsuki",
        "AnimeSeries1": "Haikyuu!!", "AnimeSeries2": "My Hero Academia", "AnimeSeries3": "Fullmetal Alchemist", "AnimeSeries4": "Dragon Ball Z", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Nick Fury", "MarvelCharacter2": "War Machine", "MarvelCharacter3": "Colossus",
        "DCCharacter1": "Batman", "DCCharacter2": "Hawkman", "DCCharacter3": "Green Arrow",
        "Occupation1": "Manager", "Occupation2": "Lawyer", "Occupation3": "Military Officer",
        "BollywoodActor1": "Akshay Kumar", "BollywoodActor2": "Ajay Devgn", "BollywoodActor3": "Nawazuddin Siddiqui",
        "HollywoodActor1": "Tom Hanks", "HollywoodActor2": "Hugh Jackman", "HollywoodActor3": "Clint Eastwood"
    },
    {
        "PersonalityType": "ESTJ", "Gender": "Female",
        "Description": "Decisive, organized, and results-driven. ESTJs are natural leaders who value efficiency, structure, and clear expectations.",
        "FamousPerson1": "Queen Victoria", "FamousPerson2": "Maria Theresa", "FamousPerson3": "Elizabeth I", "FamousPerson4": "Catherine de Medici", "FamousPerson5": "Angela Merkel (modern equivalent)",
        "Animal1": "Elephant", "Animal2": "Lion", "Animal3": "Bear",
        "AnimeCharacter1": "Tobio Kageyama", "AnimeCharacter2": "Iida Tenya", "AnimeCharacter3": "Roy Mustang", "AnimeCharacter4": "Vegeta", "AnimeCharacter5": "Bakugo Katsuki",
        "AnimeSeries1": "Haikyuu!!", "AnimeSeries2": "My Hero Academia", "AnimeSeries3": "Fullmetal Alchemist", "AnimeSeries4": "Dragon Ball Z", "AnimeSeries5": "My Hero Academia",
        "MarvelCharacter1": "Nick Fury", "MarvelCharacter2": "War Machine", "MarvelCharacter3": "Colossus",
        "DCCharacter1": "Batman", "DCCharacter2": "Hawkman", "DCCharacter3": "Green Arrow",
        "Occupation1": "Manager", "Occupation2": "Lawyer", "Occupation3": "Military Officer",
        "BollywoodActor1": "Deepika Padukone", "BollywoodActor2": "Anushka Sharma", "BollywoodActor3": "Vidya Balan",
        "HollywoodActor1": "Meryl Streep", "HollywoodActor2": "Angelina Jolie", "HollywoodActor3": "Natalie Portman"
    },
    {
        "PersonalityType": "ESFJ", "Gender": "Male",
        "Description": "Warm, sociable, and duty-driven. ESFJs are empathetic, focused on harmony, and excel at building relationships.",
        "FamousPerson1": "King Louis IX", "FamousPerson2": "Edward VI", "FamousPerson3": "Charles I", "FamousPerson4": "Frederick William I", "FamousPerson5": "George III",
        "Animal1": "Dolphin", "Animal2": "Labrador Retriever", "Animal3": "Parrot",
        "AnimeCharacter1": "All Might", "AnimeCharacter2": "Jonathan Joestar", "AnimeCharacter3": "Soma Yukihira", "AnimeCharacter4": "Daichi Sawamura", "AnimeCharacter5": "Tanjiro Kamado",
        "AnimeSeries1": "My Hero Academia", "AnimeSeries2": "JoJo’s Bizarre Adventure", "AnimeSeries3": "Food Wars", "AnimeSeries4": "Haikyuu!!", "AnimeSeries5": "Demon Slayer",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Colossus", "MarvelCharacter3": "Beast",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Flash",
        "Occupation1": "Teacher", "Occupation2": "Event Planner", "Occupation3": "Social Worker",
        "BollywoodActor1": "Shah Rukh Khan", "BollywoodActor2": "Salman Khan", "BollywoodActor3": "Ranbir Kapoor",
        "HollywoodActor1": "Chris Evans", "HollywoodActor2": "Tom Hanks", "HollywoodActor3": "Will Smith"
    },
    {
        "PersonalityType": "ESFJ", "Gender": "Female",
        "Description": "Warm, sociable, and duty-driven. ESFJs are empathetic, focused on harmony, and excel at building relationships.",
        "FamousPerson1": "Queen Alexandra", "FamousPerson2": "Marie Antoinette", "FamousPerson3": "Isabella I of Castile", "FamousPerson4": "Empress Theodora", "FamousPerson5": "Queen Elizabeth II",
        "Animal1": "Dolphin", "Animal2": "Labrador Retriever", "Animal3": "Parrot",
        "AnimeCharacter1": "All Might", "AnimeCharacter2": "Jonathan Joestar", "AnimeCharacter3": "Soma Yukihira", "AnimeCharacter4": "Daichi Sawamura", "AnimeCharacter5": "Tanjiro Kamado",
        "AnimeSeries1": "My Hero Academia", "AnimeSeries2": "JoJo’s Bizarre Adventure", "AnimeSeries3": "Food Wars", "AnimeSeries4": "Haikyuu!!", "AnimeSeries5": "Demon Slayer",
        "MarvelCharacter1": "Captain America", "MarvelCharacter2": "Colossus", "MarvelCharacter3": "Beast",
        "DCCharacter1": "Superman", "DCCharacter2": "Nightwing", "DCCharacter3": "Flash",
        "Occupation1": "Teacher", "Occupation2": "Event Planner", "Occupation3": "Social Worker",
        "BollywoodActor1": "Katrina Kaif", "BollywoodActor2": "Priyanka Chopra", "BollywoodActor3": "Alia Bhatt",
        "HollywoodActor1": "Emma Watson", "HollywoodActor2": "Margot Robbie", "HollywoodActor3": "Natalie Portman"
    }
]

# Load data into DataFrame
df = pd.DataFrame(mbti_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for gender."""
    await update.message.reply_text(
        "Made with love and python by shimon nawaz loan. Welcome to the MBTI Personality Bot! 😊 Please tell me your gender (Male/Female):"
    )
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store gender and ask E/I question."""
    user_input = update.message.text.capitalize()
    if user_input not in ["Male", "Female"]:
        await update.message.reply_text(
            "Please enter a valid gender (Male or Female)."
        )
        return GENDER
    context.user_data["gender"] = user_input
    await update.message.reply_text(
        "Great! Question 1: Do you feel energized by social interactions (Extraverted) or prefer solitary activities (Introverted)?\n"
        "Reply with 'Extraverted' or 'Introverted'."
    )
    return EI

async def ei(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store E/I response and ask S/N question."""
    user_input = update.message.text.capitalize()
    if user_input not in ["Extraverted", "Introverted"]:
        await update.message.reply_text(
            "Please reply with 'Extraverted' or 'Introverted'."
        )
        return EI
    context.user_data["ei"] = "E" if user_input == "Extraverted" else "I"
    await update.message.reply_text(
        "Question 2: Do you focus on details and facts (Sensing) or big-picture ideas and possibilities (Intuitive)?\n"
        "Reply with 'Sensing' or 'Intuitive'."
    )
    return SN

async def sn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store S/N response and ask T/F question."""
    user_input = update.message.text.capitalize()
    if user_input not in ["Sensing", "Intuitive"]:
        await update.message.reply_text(
            "Please reply with 'Sensing' or 'Intuitive'."
        )
        return SN
    context.user_data["sn"] = "S" if user_input == "Sensing" else "N"
    await update.message.reply_text(
        "Question 3: Do you make decisions based on logic and analysis (Thinking) or emotions and values (Feeling)?\n"
        "Reply with 'Thinking' or 'Feeling'."
    )
    return TF

async def tf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store T/F response and ask J/P question."""
    user_input = update.message.text.capitalize()
    if user_input not in ["Thinking", "Feeling"]:
        await update.message.reply_text(
            "Please reply with 'Thinking' or 'Feeling'."
        )
        return TF
    context.user_data["tf"] = "T" if user_input == "Thinking" else "F"
    await update.message.reply_text(
        "Question 4: Do you prefer structure and planning (Judging) or flexibility and spontaneity (Perceiving)?\n"
        "Reply with 'Judging' or 'Perceiving'."
    )
    return JP

async def jp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store J/P response, calculate MBTI, and display results."""
    user_input = update.message.text.capitalize()
    if user_input not in ["Judging", "Perceiving"]:
        await update.message.reply_text(
            "Please reply with 'Judging' or 'Perceiving'."
        )
        return JP
    context.user_data["jp"] = "J" if user_input == "Judging" else "P"

    # Construct MBTI type
    personality_type = (
        context.user_data["ei"]
        + context.user_data["sn"]
        + context.user_data["tf"]
        + context.user_data["jp"]
    )
    gender = context.user_data["gender"]

    # Query DataFrame
    result = df[
        (df["PersonalityType"] == personality_type) & (df["Gender"] == gender)
    ]
    if not result.empty:
        row = result.iloc[0]
        response = (
            f"🎉 Your MBTI Personality Type is *{personality_type}*!\n\n"
            f"**Description**: {row['Description']}\n\n"
            f"**Famous { 'Kings' if gender == 'Male' else 'Queens' }**: "
            f"{', '.join(row[['FamousPerson1', 'FamousPerson2', 'FamousPerson3', 'FamousPerson4', 'FamousPerson5']])}\n\n"
            f"**Animals**: {', '.join(row[['Animal1', 'Animal2', 'Animal3']])}\n\n"
            f"**Anime Characters**: "
            f"{row['AnimeCharacter1']} ({row['AnimeSeries1']}), "
            f"{row['AnimeCharacter2']} ({row['AnimeSeries2']}), "
            f"{row['AnimeCharacter3']} ({row['AnimeSeries3']}), "
            f"{row['AnimeCharacter4']} ({row['AnimeSeries4']}), "
            f"{row['AnimeCharacter5']} ({row['AnimeSeries5']})\n\n"
            f"**Marvel Characters**: {', '.join(row[['MarvelCharacter1', 'MarvelCharacter2', 'MarvelCharacter3']])}\n\n"
            f"**DC Characters**: {', '.join(row[['DCCharacter1', 'DCCharacter2', 'DCCharacter3']])}\n\n"
            f"**Best Occupations**: {', '.join(row[['Occupation1', 'Occupation2', 'Occupation3']])}\n\n"
            f"**Bollywood { 'Actors' if gender == 'Male' else 'Actresses' }**: "
            f"{', '.join(row[['BollywoodActor1', 'BollywoodActor2', 'BollywoodActor3']])}\n\n"
            f"**Hollywood { 'Actors' if gender == 'Male' else 'Actresses' }**: "
            f"{', '.join(row[['HollywoodActor1', 'HollywoodActor2', 'HollywoodActor3']])}"
        )
    else:
        response = (
            f"Sorry, no data found for {personality_type} and gender {gender}. "
            "Please try again with /start."
        )

    await update.message.reply_text(response, parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "Personality test cancelled. Use /start to try again!"
    )
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Run the bot."""
    # Initialize the bot with the provided token
    application = Application.builder().token("7912867191:AAFm0zmehPk53bRVcAC8iZY9V-ztIhzONWA").build()

    # Set up ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            EI: [MessageHandler(filters.TEXT & ~filters.COMMAND, ei)],
            SN: [MessageHandler(filters.TEXT & ~filters.COMMAND, sn)],
            TF: [MessageHandler(filters.TEXT & ~filters.COMMAND, tf)],
            JP: [MessageHandler(filters.TEXT & ~filters.COMMAND, jp)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
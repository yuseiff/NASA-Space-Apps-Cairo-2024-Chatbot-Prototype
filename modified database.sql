CREATE DATABASE NASA_Hackathon_Challenges;
USE NASA_Hackathon_Challenges;

-- Create Challenges table
CREATE TABLE IF NOT EXISTS Challenges (
    ChallengeID INT AUTO_INCREMENT PRIMARY KEY,
    ChallengeName VARCHAR(255),
    ChallengeSummary TEXT
);

-- Create PotentialConsiderations table
CREATE TABLE IF NOT EXISTS PotentialConsiderations (
    ConsiderationID INT AUTO_INCREMENT PRIMARY KEY,
    ChallengeID INT,
    Consideration TEXT,
    FOREIGN KEY (ChallengeID) REFERENCES Challenges(ChallengeID)
);

-- Create OutcomesTopics table
CREATE TABLE IF NOT EXISTS OutcomesTopics (
    OutcomeTopicID INT AUTO_INCREMENT PRIMARY KEY,
    ChallengeID INT,
    OutcomeTopic VARCHAR(255),
    FOREIGN KEY (ChallengeID) REFERENCES Challenges(ChallengeID)
);

-- Select data from Challenges table
SELECT * FROM Challenges;

-- Select data from PotentialConsiderations table
SELECT * FROM PotentialConsiderations;

-- Select data from OutcomesTopics table
SELECT * FROM OutcomesTopics;

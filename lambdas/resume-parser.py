import os
import sys
import subprocess
import pdfminer
import pdfminer.high_level
from collections import Counter
# os.system('pip3 install nltk -t /tmp/ --no-cache-dir')
# sys.path.insert(1, '/tmp/')
import re
import nltk
from nltk.corpus import stopwords
import string
from nltk import word_tokenize
import json
import boto3
from io import BytesIO
import requests


def lambda_handler(event, context):
    # TODO implement
    
    # print(event)
    # print("--------S3 Trigger--------------------")
    # print(event["Records"][0])
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    name = event["Records"][0]["s3"]["object"]["key"]
    s3_resource = boto3.resource('s3')
    obj = s3_resource.Object(bucket_name=bucket, key=name)
    
    user_name=obj.get()['Metadata']['name']
    
    user_logInEmailId= obj.get()['Metadata']['loginemail']
    access_token = obj.get()['Metadata']['access_token']
    # print("---------------current user details------------")
    # print(user_name)
    print(user_logInEmailId)
    
    fs = obj.get()['Body'].read()
    # print("HEY")
    resume = pdfminer.high_level.extract_text(BytesIO(fs))
    table = boto3.resource('dynamodb',region_name='us-east-1', aws_access_key_id=' ', aws_secret_access_key='  ').Table("skillset")
    #obtainedResumeText = fileTextExtractor(resume)
    obtainedResumeText= resume
    # print("-------------------------------------", obtainedResumeText)
    final = personalDetailExtractor(obtainedResumeText)
    print("---------------personal details----------------")
    # print("Email Address:",final[0])
    # print("Phone Number:",final[1])
    
    firstLetterCapitalizedText,obtainedResumeTextLowerCase,obtainedResumeTextUpperCase = CapitalizeFirstLetter(obtainedResumeText)
    obtainedResumeText = obtainedResumeTextLowerCase + obtainedResumeTextUpperCase + firstLetterCapitalizedText
    obtainedResumeText = re.sub(r'\d+','',obtainedResumeText)
    obtainedResumeText = obtainedResumeText.translate(str.maketrans('','',string.punctuation))
    # print("------------------trying----------",obtainedResumeText)
    # print("-------------------------------------", obtainedResumeText)
    
    try:
        print("-----------in try-------------")
        # educationLevelList= table.get_item(Key={'skill_d':'education'})
        resumeTechnicalSkillSpecificationList= table.get_item(Key={'skill_d':'skill'})

    except Exception as e:
        print(e)
        
        
    # extractedEducatioDetails = EducationDetailsExtractor(obtainedResumeText, educationLevelList['Item']['skillname'])
    # print("Academic Qualifications:",extractedEducatioDetails)
    filteredTextForSkillExtraction = stopWordRemoval(obtainedResumeText)
    print("---------------filtered text--------------")
    # resumeTechnicalSkillSpecificationList= {'skill':skills }
    # print(resumeTechnicalSkillSpecificationList)
    technicalSkillScore , technicalSkillExtracted = ResumeSkillExtractor( resumeTechnicalSkillSpecificationList['Item']['skills'],filteredTextForSkillExtraction)
    print("skills:", technicalSkillExtracted)
    print("score:", technicalSkillScore)
    document = parseForDynamoDB(user_name,user_logInEmailId, final[0],final[1],technicalSkillExtracted, technicalSkillScore)
    print(document)
    response = indexIntoDB(document, name)
    return {
        'statusCode': 200,
        'body': response
    }
    

def personalDetailExtractor(obtainedResumeText):
    finalExtractedEmail = []
    resumeFinalPhone = []
    oneFourthOfResume = obtainedResumeText[0:len(obtainedResumeText)//4]
    emailResume = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", oneFourthOfResume)
    phoneResume = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})",oneFourthOfResume)
    if len(emailResume) > 1:
        finalExtractedEmail = emailResume[0]
    else:
        finalExtractedEmail = emailResume
    # print(finalExtractedEmail)
    for i in range(len(phoneResume)):
        if len(phoneResume[i])>=10:
            resumeFinalPhone = phoneResume[i]
    # print(resumeFinalPhone)
    return [finalExtractedEmail,resumeFinalPhone]



firstLetterCapitalizedObtainedResumeText = []
def CapitalizeFirstLetter(obtainedResumeText):
    capitalizingString = " "
    obtainedResumeTextLowerCase = obtainedResumeText.lower()
    obtainedResumeTextUpperCase = obtainedResumeText.upper()
    splitListOfObtainedResumeText = obtainedResumeText.split()
    for i in splitListOfObtainedResumeText:
        firstLetterCapitalizedObtainedResumeText.append(i.capitalize())
    return (capitalizingString.join(firstLetterCapitalizedObtainedResumeText),obtainedResumeTextLowerCase,obtainedResumeTextUpperCase)



def EducationDetailsExtractor(obtainedResumeText, educationLevelList):
    obtainedResumeText.strip('/n')
    newLineRemovedResumeText = obtainedResumeText
    resumeEducationSpecificationList = {'Education':educationLevelList}
    educationExtracted = []
    for area in resumeEducationSpecificationList.keys():
        if area == 'Education':
            educationWord = []
            for word in resumeEducationSpecificationList[area]:
                w1=""
                for w in word.split():
                    if w in obtainedResumeText:
                        w1 += "".join(w+" ")
                educationWord.append(w1)
            for value in educationWord:
                if value.strip() in resumeEducationSpecificationList[area]:
                    educationExtracted.append(value.strip())
    return educationExtracted


def stopWordRemoval(obtainedResumeText):
    # nltk.download('stopwords')
    stop_words = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])
    word_tokens = obtainedResumeText.split()
    # print(word_tokens)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    joinEmptyString = " "
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return(joinEmptyString.join(filtered_sentence))



def ResumeSkillExtractor(resumeTechnicalSkillSpecificationList,filteredTextForSkillExtraction):
    skillScores =0
    skillExtracted = []
    for word in resumeTechnicalSkillSpecificationList:
        if word in filteredTextForSkillExtraction:
            skillExtracted.append(word)
            skillScores +=1
    return skillScores,skillExtracted

def indexIntoDB(document, name):
    

        
        
    tableUser = boto3.resource('dynamodb',region_name='us-east-1', aws_access_key_id=' ', aws_secret_access_key='  ').Table("UserData")
    try:
        r = tableUser.update_item(
                        Key={
                            'email':document['User_LoggedInEmail']
                          },
                           UpdateExpression="set phone= :st, skills= :usr",
        ExpressionAttributeValues={
            ':st' : document['Phone'],
            ':usr' : document['skills']
                }
            #               ExpressionAttributeValues={
            # 'phone' : document['Phone'],
            # 'skills' : document['skills']
            #     }
                          )
    except Exception as e:
        print(e)
        
    return r
    
def parseForDynamoDB(user_name,user_logInEmailId,finalExtractedEmail,finalExtractedPhone,technicalSkillExtracted, technicalSkillScore):
    document = {
            "UserName": user_name,
            "User_LoggedInEmail": user_logInEmailId,
            "Email" : finalExtractedEmail,
            "Phone" : finalExtractedPhone,
            # "Education": extractedEducatioDetails,
            "skills": technicalSkillExtracted,
            "score" : technicalSkillScore
    }
    return document




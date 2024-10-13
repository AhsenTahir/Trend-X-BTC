import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const splitSql = (sql: string) => {
  return sql.split(';').filter(content => content.trim() !== '')
}

async function main() {
  const sql = `

INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('d3c71b73-9e7d-4723-a50e-303c41b7a414', '1Letitia_Morissette94@gmail.com', 'Bob Brown', 'https://i.imgur.com/YfJQV5z.png?id=3', 'inv11223', false, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('f0b1568d-4711-4950-b97a-00a2fc25e230', '10Rhett.Casper-Hickle@hotmail.com', 'Alice Jones', 'https://i.imgur.com/YfJQV5z.png?id=12', 'inv54321', true, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d', '19Casimir.Durgan@yahoo.com', 'Bob Brown', 'https://i.imgur.com/YfJQV5z.png?id=21', 'inv67890', true, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('a35a235d-3093-40df-84a5-1df5f9449783', '28Lucio_Connelly@hotmail.com', 'Charlie Davis', 'https://i.imgur.com/YfJQV5z.png?id=30', 'inv12345', false, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('493175cd-e8b5-41c2-be98-67ffee97199d', '37Loraine_Huel65@yahoo.com', 'Jane Smith', 'https://i.imgur.com/YfJQV5z.png?id=39', 'inv12345', true, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('a6c57822-9edd-42bb-b6c9-963608f38334', '46Sid_Kuvalis@gmail.com', 'Jane Smith', 'https://i.imgur.com/YfJQV5z.png?id=48', 'inv67890', false, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('6ae9b91d-eb12-41da-960b-a07b5019c359', '55Cameron_Crooks@gmail.com', 'Charlie Davis', 'https://i.imgur.com/YfJQV5z.png?id=57', 'inv11223', true, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('20f85057-8f45-465c-91da-e3dca96e76af', '64Denis_Hamill8@yahoo.com', 'Alice Jones', 'https://i.imgur.com/YfJQV5z.png?id=66', 'inv09876', true, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');
INSERT INTO "User" ("id", "email", "name", "pictureUrl", "tokenInvitation", "emailVerified", "status", "globalRole", "password") VALUES ('6548ed94-add4-41ca-8393-04aa6f3fe100', '82Camille_Gutkowski-Wiza54@hotmail.com', 'Jane Smith', 'https://i.imgur.com/YfJQV5z.png?id=84', 'inv12345', false, 'VERIFIED', 'USER', '$2b$10$ppubsZypHzkqW9dkhMB97ul2.wSsvaCoDE2CzqIHygddRMKXvpYUC');

INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('b881ab41-1882-447e-92f5-9b29a1726c8a', 'a1b2c3d4e5f6g7h8i9j0', '{"adflicto":"paens","bis":"terror","defetiscor":"curis","xiphias":"synagoga"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('f955afa9-0c9b-4b06-a240-e8d57978ba4c', 'l9k8j7h6g5f4d3s2a1z0', '{"chirographum":"tibi","triduana":"adfectus","consectetur":"crudelis","thesaurus":"animadverto"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('7ecd5e2f-2c54-44f9-aef0-06dd5a63e09b', 'm1n2b3v4c5x6z7a8s9d0', '{"vulnero":"stabilis","caste":"vinum","varietas":"contra","comedo":"viscus"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('a02fd09e-6799-4293-80c1-0f677b776d36', 'l9k8j7h6g5f4d3s2a1z0', '{"aqua":"tenuis","vilicus":"claro","demergo":"absorbeo"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('96ca7232-27a9-41d1-a78c-82722f3a2117', 'z9y8x7w6v5u4t3s2r1q0', '{"aequitas":"ademptio","vester":"dapifer","calcar":"quae","conitor":"thorax","surgo":"compono"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('212a3156-08f7-476a-a035-b79f7eba76d9', 'm1n2b3v4c5x6z7a8s9d0', '{"comprehendo":"tamen","barba":"ventosus","undique":"suscipit","expedita":"quas"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('f9c9b8fd-430b-482b-aed9-eae5b7711a87', 'a1b2c3d4e5f6g7h8i9j0', '{"adfectus":"aegrus","verto":"officia","adhaero":"ad"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('13afe370-3178-4310-ad26-05255bb091c3', 'l9k8j7h6g5f4d3s2a1z0', '{"canto":"arbor","aqua":"patrocinor","arx":"corpus"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('c026e0eb-e3a3-4cc2-babd-f7a39381fc92', 'l9k8j7h6g5f4d3s2a1z0', '{"coma":"caveo","cultura":"abscido","cetera":"in","tactus":"textus"}'::jsonb);
INSERT INTO "RagVector" ("id", "key", "tags") VALUES ('29eea022-6ead-4cd2-b435-dbae119e5e9c', 'z9y8x7w6v5u4t3s2r1q0', '{"turba":"cui","usque":"conduco","certus":"terror","creator":"deinde","titulus":"vix"}'::jsonb);

INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('ca877929-0be7-49b2-a357-7c886e794908', 'Crypto Insights LLC', 'https://i.imgur.com/YfJQV5z.png?id=122');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('9e6ab617-8a4c-427b-a588-8a62603b6191', 'Crypto Insights LLC', 'https://i.imgur.com/YfJQV5z.png?id=125');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('4027311d-61ef-4b5e-a227-3b0809507d63', 'Blockchain Ventures Inc', 'https://i.imgur.com/YfJQV5z.png?id=128');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('1c2ed2b2-8373-4205-82cd-51fad27b5b72', 'Blockchain Ventures Inc', 'https://i.imgur.com/YfJQV5z.png?id=131');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('bec4bb04-9be7-4c0f-8000-1a1ce7c1449a', 'Digital Currency Group', 'https://i.imgur.com/YfJQV5z.png?id=134');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('6228511e-b573-43ca-9f81-83db22c5dafa', 'Satoshi Solutions', 'https://i.imgur.com/YfJQV5z.png?id=137');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('ab4066a2-a0f3-43b9-8336-d389a49e6dd7', 'Digital Currency Group', 'https://i.imgur.com/YfJQV5z.png?id=140');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('afb3da45-bd25-4a7a-834b-73982dd0bb02', 'Crypto Insights LLC', 'https://i.imgur.com/YfJQV5z.png?id=143');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('a2691669-3cd8-413b-ae89-252e4c0c1369', 'Crypto Insights LLC', 'https://i.imgur.com/YfJQV5z.png?id=146');
INSERT INTO "Organization" ("id", "name", "pictureUrl") VALUES ('bfd8d0a3-7b92-42da-8da3-17ce127a1839', 'Bitcoin Analytics Co', 'https://i.imgur.com/YfJQV5z.png?id=149');

INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('e0f1c0fe-05b7-437a-9e5c-0e9c54abb7be', 'Cryptocurrency Trader', '493175cd-e8b5-41c2-be98-67ffee97199d', '4027311d-61ef-4b5e-a227-3b0809507d63');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('d1d5e67b-a7f5-4ae4-ac13-3fceb0da19ac', 'Blockchain Developer', 'a6c57822-9edd-42bb-b6c9-963608f38334', '1c2ed2b2-8373-4205-82cd-51fad27b5b72');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('e5de401f-db0f-4450-b911-d825de67f7d8', 'Market Strategist', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc', 'ab4066a2-a0f3-43b9-8336-d389a49e6dd7');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('1f733eed-7369-4c2c-bf95-b4091fbeaf9e', 'Blockchain Developer', 'a6c57822-9edd-42bb-b6c9-963608f38334', '6228511e-b573-43ca-9f81-83db22c5dafa');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('90cdbbbc-7baf-40f4-961b-d4f3e29c339d', 'Cryptocurrency Trader', '6ae9b91d-eb12-41da-960b-a07b5019c359', 'afb3da45-bd25-4a7a-834b-73982dd0bb02');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('b5485f24-94ae-4f81-a2e2-3269d4c15ded', 'Blockchain Developer', '6548ed94-add4-41ca-8393-04aa6f3fe100', '9e6ab617-8a4c-427b-a588-8a62603b6191');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('da300662-c08c-462c-bfcb-fe8401b38595', 'Market Strategist', 'd3c71b73-9e7d-4723-a50e-303c41b7a414', 'ab4066a2-a0f3-43b9-8336-d389a49e6dd7');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('199456bd-09ee-4a0b-a3fc-4f444716b5b9', 'Market Strategist', 'e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d', '9e6ab617-8a4c-427b-a588-8a62603b6191');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('c3756d57-9560-4a0e-9a28-2a06a31d9759', 'Cryptocurrency Trader', 'a6c57822-9edd-42bb-b6c9-963608f38334', 'ca877929-0be7-49b2-a357-7c886e794908');
INSERT INTO "OrganizationRole" ("id", "name", "userId", "organizationId") VALUES ('ccee2b6f-0e9b-4422-a384-84993c91c7be', 'Market Strategist', '493175cd-e8b5-41c2-be98-67ffee97199d', '4027311d-61ef-4b5e-a227-3b0809507d63');

INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('2b5b07b6-dc6e-4acc-9513-c125699c3c18', 'httpsapi.example.comnotify1', 'sub_0987654321fedcba', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('86b97fda-6200-45f3-8288-57f411e6846f', 'httpsapi.example.comnotify5', 'sub_1234567890abcdef', '493175cd-e8b5-41c2-be98-67ffee97199d');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('22cd311a-0955-408a-a9a7-4f6321c057b0', 'httpsapi.example.comnotify5', 'sub_fedcba0987654321', 'a35a235d-3093-40df-84a5-1df5f9449783');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('1a869458-4ec7-4d3c-80f3-59c831b92c92', 'httpsapi.example.comnotify3', 'sub_fedcba0987654321', 'a35a235d-3093-40df-84a5-1df5f9449783');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('db37b93c-7df7-4980-9adf-fba5f669ef1f', 'httpsapi.example.comnotify4', 'sub_1234567890abcdef', '493175cd-e8b5-41c2-be98-67ffee97199d');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('1d8dd85c-e2cf-439b-99b8-ac576e0ebd6b', 'httpsapi.example.comnotify2', 'sub_fedcba0987654321', '6ae9b91d-eb12-41da-960b-a07b5019c359');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('cfcce2c6-580c-4414-940c-84c949264aef', 'httpsapi.example.comnotify1', 'sub_1122334455667788', '493175cd-e8b5-41c2-be98-67ffee97199d');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('1b508d31-18b8-4e6a-b9f9-923d95319c7c', 'httpsapi.example.comnotify4', 'sub_1122334455667788', 'e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('ee6d3a2b-b70b-4ff6-bc3a-3c560c63a731', 'httpsapi.example.comnotify4', 'sub_0987654321fedcba', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc');
INSERT INTO "PushNotification" ("id", "endpoint", "subscription", "userId") VALUES ('b449787d-79fc-4bb2-9d5e-e4b9859f1c05', 'httpsapi.example.comnotify5', 'sub_0987654321fedcba', 'a35a235d-3093-40df-84a5-1df5f9449783');

INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('974492de-c998-45f0-82df-0cbff61c0ed4', 'BTC', 172, '46000.56', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc', 'bfd8d0a3-7b92-42da-8da3-17ce127a1839');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('ed49e7b8-61c7-4644-87cc-0fe36e57a964', 'BTCEUR', 136, '49000.34', '6548ed94-add4-41ca-8393-04aa6f3fe100', '4027311d-61ef-4b5e-a227-3b0809507d63');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('57c6aab8-4065-4931-8b41-827fd92bf472', 'BTCEUR', 288, '49000.34', '6ae9b91d-eb12-41da-960b-a07b5019c359', '6228511e-b573-43ca-9f81-83db22c5dafa');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('30694189-432f-40a9-8095-69f352a7008f', 'BTCEUR', 92, '49000.34', 'd3c71b73-9e7d-4723-a50e-303c41b7a414', '6228511e-b573-43ca-9f81-83db22c5dafa');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('f5ce3875-e811-4e28-8670-e2c3b67bebff', 'BTC', 190, '46000.56', '20f85057-8f45-465c-91da-e3dca96e76af', '1c2ed2b2-8373-4205-82cd-51fad27b5b72');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('5758945f-2cff-4367-925e-3529268583df', 'BTCUSD', 217, '46000.56', 'd3c71b73-9e7d-4723-a50e-303c41b7a414', 'ca877929-0be7-49b2-a357-7c886e794908');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('a0a78538-478e-40e4-a9e5-2df4132349ed', 'XBT', 380, '48000.12', 'f0b1568d-4711-4950-b97a-00a2fc25e230', 'bec4bb04-9be7-4c0f-8000-1a1ce7c1449a');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('13928668-daa0-40a7-aff8-867c58dc0b74', 'BTCEUR', 720, '47000.89', '493175cd-e8b5-41c2-be98-67ffee97199d', 'bfd8d0a3-7b92-42da-8da3-17ce127a1839');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('4ccb41dc-2e72-4885-989a-dfa11bd793de', 'BTCGBP', 98, '48000.12', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc', 'bec4bb04-9be7-4c0f-8000-1a1ce7c1449a');
INSERT INTO "Prediction" ("id", "bitcoinSymbol", "windowSize", "predictionData", "userId", "organizationId") VALUES ('1f8da360-0a12-4f96-8239-ef252728b39e', 'BTCGBP', 899, '49000.34', '20f85057-8f45-465c-91da-e3dca96e76af', '6228511e-b573-43ca-9f81-83db22c5dafa');

INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('2ce4bd24-5383-409f-9fad-5118ee06f12c', 'Jane Smith', '242Isabelle49@yahoo.com', 'Feature Request', 'I would like to suggest a new feature for the prediction page.', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('19a64650-0a90-4314-996e-b83cfc111f7f', 'Emily Davis', '247Irving44@yahoo.com', 'API Documentation Inquiry', 'I would like to suggest a new feature for the prediction page.', 'e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('3cb79b43-1de4-4f13-94b9-63342fe26990', 'Emily Davis', '252Elyssa.Osinski@gmail.com', 'General Inquiry', 'Could you provide more details on the predict endpoint', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('38f2cb16-27b9-4b30-9a4c-d27388c1ec05', 'Jane Smith', '257Harold18@gmail.com', 'Bitcoin Price Prediction', 'Could you provide more details on the predict endpoint', 'e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('9e627e17-1503-4d06-8b82-de046a2669ad', 'Alice Johnson', '262Jan.Howe62@gmail.com', 'Bitcoin Price Prediction', 'I have a question about the market news API integration.', 'e4587d4c-f9e0-42ec-8b8c-9121a4d6cd9d');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('c62c7fda-02bc-4df4-997a-19c84e5c51ab', 'John Doe', '267Kobe_Orn60@hotmail.com', 'General Inquiry', 'Could you provide more details on the predict endpoint', 'f0b1568d-4711-4950-b97a-00a2fc25e230');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('8acbeef8-2402-42c3-9015-b832327e3a72', 'John Doe', '272Willard.Hoppe4@hotmail.com', 'Website Feedback', 'I have a question about the market news API integration.', '20f85057-8f45-465c-91da-e3dca96e76af');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('628892cb-2700-4be5-9b27-161c50243d94', 'Bob Brown', '277Aubree46@yahoo.com', 'Website Feedback', 'I am interested in learning more about your Bitcoin price prediction model.', '20f85057-8f45-465c-91da-e3dca96e76af');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('9f8c6e56-ec50-462d-8c78-9b09e183a08e', 'Alice Johnson', '282Vesta.Nikolaus75@hotmail.com', 'Feature Request', 'I have a question about the market news API integration.', '6ae9b91d-eb12-41da-960b-a07b5019c359');
INSERT INTO "ContactMessage" ("id", "name", "email", "subject", "message", "userId") VALUES ('321e50e4-5c84-4e7a-be42-ec25233a9b47', 'Emily Davis', '287Delfina.Goyette13@yahoo.com', 'Website Feedback', 'The website looks great I love the dark theme.', '21a857f1-ba5f-4435-bcf6-f910ec07c0dc');

  `

  const sqls = splitSql(sql)

  for (const sql of sqls) {
    try {
      await prisma.$executeRawUnsafe(`${sql}`)
    } catch (error) {
      console.log(`Could not insert SQL: ${error.message}`)
    }
  }
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async error => {
    console.error(error)
    await prisma.$disconnect()
    process.exit(1)
  })

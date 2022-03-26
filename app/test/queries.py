# # 1 - imports
# from user import User
# from base import Session
# from article import Article

# # 2 - extract a session
# session = Session()

# # 3 - extract all movies
# news = session.query(Article).all()
# users = session.query(User).all()
# # 4 - print movies' details
# print('\n### All news:')
# for article in news:
#     print(f'key : {article.id}\ntitle : {article.title}\nreleased : {article.release_date}')
#     print('\n')



# print('\n### Filter check')
# key = "cme-bitcoin-derivative-traders-had-paper-hands-as-btc-broke-55k-report"
# key = "bitcoin-s-250k-resistance-to-become-support-in-q4-bloomberg-commodity-strategist"
# print(f'key: {key}')
# print(session.query(session.query(Article).filter_by(id = key).exists()).scalar())

# print('\n### User check')
# session.query(User).filter_by(id = 1413049174).first().status = "inactive"
# print("User leaved channel")
# session.commit()

# print('\n### All users:')
# for user in users:    
#     print(f'{user.id} was registered on {user.time_created} : {user.status} - last seen: {user.last_seen}')
#     # print('\n')
    
# session.close()
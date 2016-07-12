# coding: utf-8
import ticketdata.predict as prd
from ticketdata.dbqueries import get_games_froms
from datetime import datetime




date_cutoffs = [
	datetime(2016,7,12), 
	datetime(2016,8,1),
	datetime(2016,8,3),
	datetime(2016,8,6),
	datetime(2016,8,10),
	datetime(2016,8,15),
	datetime(2016,8,20),
	datetime(2016,9,1),
	datetime(2016,9,10),
	datetime(2016,9,20),
	datetime(2016,9,27),
	datetime(2016,10,10)
	]

def make_csv_name_for_daterange(date1, date2):
    date1str = datetime.strftime(date1, '%m%d')
    date2str = datetime.strftime(date2, '%m%d')
    return 'pred{}_{}.csv'.format(date1str, date2str)

def get_all():
	for i in range(len(date_cutoffs)-1):
		date_range = get_games_froms(date_cutoffs[i], date_cutoffs[i+1])
		prd.prep_for_predict(date_range, make_csv_name_for_daterange(date_cutoffs[i], date_cutoffs[i+1]))



if __name__ == '__main__':
	
	input0 = ''
	while input0 not in {'predictions', 'models'}:
		input0 = raw_input('Type "predictions" or "models":\n  >')


	if input0 == 'predictions':
		print "Let's get the predictions data going then! Starting up..."
		input1 = ''
		while input1 not in {'all', 'choices'}:
			input1 = raw_input('Type "all" or "choices":\n  >')

		if input1 == 'all':
			print 'All! Starting up...'.format(input2)
			get_all()
		else:
			for i in range(len(date_cutoffs)-1):
				print '{} : {}'.format(i+1,make_csv_name_for_daterange(date_cutoffs[i], date_cutoffs[i+1]))
			input2 = 0
			print range(1,len(date_cutoffs)+1)
			while input2 not in range(1,len(date_cutoffs)):
				try:
					input2 = int(raw_input('Enter the number of the choice you want:\n  >'))
				except:
					pass
			print 'Choice {}! Starting up...'.format(input2)
			print date_cutoffs[input2-1], date_cutoffs[input2]
			date_range = get_games_froms(date_cutoffs[input2-1], date_cutoffs[input2])
			# print date_range
			prd.prep_for_predict(date_range, make_csv_name_for_daterange(date_cutoffs[input2-1], date_cutoffs[input2]))
	else:
		print 'Models it is! Starting up...'
		print 'STARTING MODEL 1...'
		modset1 = prd.prep_for_model('model1.csv', prd.basic_threshes)
		print 'STARTING MODEL 2...'
		modset2 = prd.prep_for_model('model2.csv', prd.semi_basic_threshes)
		print 'STARTING MODEL 3...'
		modset3 = prd.prep_for_model('model3.csv', prd.less_basic_threshes)
		print 'STARTING MODEL 4...'
		modset4 = prd.prep_for_model('model4.csv', prd.threshes_4)
		print 'STARTING MODEL 5...'
		modset5 = prd.prep_for_model('model5.csv', prd.threshes_5)

# july_dates = get_games_froms(datetime.utcnow(), datetime(2016,8,1))
# pred0708_0731= prd.prep_for_predict(july_dates,'pred0708_0731.csv')


# aug_1_3_dates = get_games_froms(datetime(2016,8,1), datetime(2016,8,3))
# pred_0801_0803 = prd.prep_for_predict(aug_1_3_dates, 'pred0801_0803.csv')


# next_dates_3 = get_games_froms(datetime(2016,8,3), datetime(2016,8,6))
# pred_0803_0806 = prd.prep_for_predict(next_dates_3, 'pred0803_0806.csv')


# next_dates_4 = get_games_froms(datetime(2016,8,6), datetime(2016,8,10))
# pred_0806_0810 = prd.prep_for_predict(next_dates_4, 'pred0806_0810.csv')


# next_dates_5 = get_games_froms(datetime(2016,8,10), datetime(2016,8,15))
# pred_0810_0815 = prd.prep_for_predict(next_dates_5, 'pred0810_0815.csv')


# next_dates_6 = get_games_froms(datetime(2016,8,15), datetime(2016,8,20))
# pred_0815_0820 = prd.prep_for_predict(next_dates_6, 'pred0815_0820.csv')


# next_dates_7 = get_games_froms(datetime(2016,8,20), datetime(2016,9,1))
# pred_0820_0901 = prd.prep_for_predict(next_dates_7, 'pred0820_0901.csv')


# next_dates_8 = get_games_froms(datetime(2016,9,1), datetime(2016,9,10))
# pred_0901_0910 = prd.prep_for_predict(next_dates_8, 'pred_0901_0910.csv')


# next_dates_9 = get_games_froms(datetime(2016,9,10), datetime(2016,9,20))
# pred_0910_0920 = prd.prep_for_predict(next_dates_9, 'pred_0910_0920.csv')


# next_dates_10 = get_games_froms(datetime(2016,9,20), datetime(2016,9,27))
# pred_0920_0927 = prd.prep_for_predict(next_dates_10, 'pred_0920_0927.csv')


# next_dates_11 = get_games_froms(datetime(2016,9,27), datetime(2016,10,10))
# pred_0927_1010 = prd.prep_for_predict(next_dates_11, 'pred_0927_1010.csv')


# modset1 = prd.prep_for_model('model1.csv', prd.basic_threshes)
# modset2 = prd.prep_for_model('model2.csv', prd.semi_basic_threshes)
# modset3 = prd.prep_for_model('model3.csv', prd.less_basic_threshes)
# modset4 = prd.prep_for_model('model4.csv', prd.threshes_4)
# modset5 = prd.prep_for_model('model5.csv', prd.threshes_5)

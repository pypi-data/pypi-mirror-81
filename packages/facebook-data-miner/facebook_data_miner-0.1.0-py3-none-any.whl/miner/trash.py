# from miner.utils import const
#
#
# class Report:
#     def __init__(self, analyzer) -> None:
#         self.content = []
#         self.data = ReportDataAdapter(analyzer)
#         self.transform_data()
#
#     def transform_data(self):
#         self.fill_content()
#         # self.get_ranking_data()
#
#     def print(self):
#         for key, value in self.content:
#             print(f"{key}: {value}")
#
#     def add_content(self, text, stat):
#         self.content.append((text, stat,))
#
#     def get_ranking_data(self):
#         ranking = self.data.get_ranking(stat="mc")
#         self.add_content("")
#
#     def fill_content(self):
#         for name, stat in self.data.get_basic_stats():
#             self.add_content(f"{name} count", f"{stat:,}")
#         for name, stat in self.data.get_unique_stats():
#             self.add_content(f"{name} count", f"{stat:,}")
#         print(40 * "-")
#         self.fill_stat_per_period_data(stat="mc")
#         print(40 * "-")
#         self.fill_stat_per_period_data(stat="wc")
#         print(40 * "-")
#         self.fill_stat_per_period_data(stat="cc")
#         print(40 * "-")
#
#     def fill_stat_per_period_data(self, stat="mc"):
#         self.add_content("Time period statistic", const.STAT_MAP.get(stat))
#         for time, stat in self.data.get_stat_per_period_data(stat=stat):
#             self.add_content(time, stat)
#
#
# class ReportDataAdapter:
#     def __init__(self, analyzer):
#         self.analyzer = analyzer
#
#     def get_ranking(self, stat="mc"):
#         return self.analyzer.get_ranking_of_friends_by_message_stats(stat=stat)
#
#     def get_basic_stats(self):
#         for name in const.STAT_MAP.keys():
#             readable = const.STAT_MAP.get(name)
#             stat = getattr(self.analyzer._stats, name)
#             yield readable, stat
#
#     def get_unique_stats(self):
#         yield "Unique message", self.analyzer.priv_stats.unique_mc
#         yield "Unique word", self.analyzer.priv_stats.unique_wc
#
#     def get_stat_per_period_data(self, stat="mc"):
#         for timeframe in ["y", "m", "d", "h"]:
#             # for period in ['y',]:
#             data = self.analyzer._stats.stats_per_timeframe(timeframe, statistic=stat)
#             for year, count in data.items():
#                 yield year, f"{count:,}"


# Plotter CLI
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Visualize chat statistics")
#     parser.add_argument(
#         "-p",
#         "--path",
#         metavar="path",
#         type=str,
#         default=DATA_PATH,
#         help="Path to the data folder.",
#     )
#     parser.add_argument(
#         "-k",
#         "--kind",
#         metavar="kind",
#         type=str,
#         default="private",
#         help="private or group",
#     )
#     parser.add_argument(
#         "-t",
#         "--typ",
#         metavar="typ",
#         type=str,
#         default="ranking",
#         help="One of {series|stats|ranking|type}, standing for time series, stats per period, ranking of friends by messages and type of messages.",
#     )
#     parser.add_argument(
#         "-tf",
#         "--timeframe",
#         metavar="timeframe",
#         type=str,
#         default="y",
#         help="One of {y|m|d|h}, standing for yearly, monthly, daily and hourly breakdown of statisctics.",
#     )
#     parser.add_argument(
#         "-S",
#         "--stat",
#         metavar="stat",
#         type=str,
#         default="mc",
#         help="One of {msg|word|char}, indicating which statistics do you want to get.",
#     )
#     parser.add_argument(
#         "-c",
#         "--channels",
#         metavar="channels",
#         type=str,
#         default=None,
#         help="A channels's name.",
#     )
#     parser.add_argument(
#         "-pa",
#         "--participants",
#         metavar="participants",
#         type=str,
#         default=None,
#         help="Filter for conversations where `participants`' value is a participant.",
#     )
#     parser.add_argument(
#         "-s",
#         "--senders",
#         metavar="senders",
#         type=str,
#         default="all",
#         help="Filter for `senders`' messages (can be `all`,`me`, `partner` or any name you know of).",
#     )
#     parser.add_argument(
#         "-fr",
#         "--from",
#         metavar="from",
#         type=str,
#         default=None,
#         help="Start date in format %Y-%m-%d",
#     )
#     parser.add_argument(
#         "-to",
#         "--to",
#         metavar="to",
#         type=str,
#         default=None,
#         help="End date in format %Y-%m-%d",
#     )
#     parser.add_argument(
#         "-pe",
#         "--period",
#         metavar="period",
#         type=str,
#         default="y",
#         help="One of {y|m|d|h}, standing for yearly, monthly, daily and hourly. Used for date filtering.",
#     )
#

#     args = parser.parse_args()
#     path = args.path
#     kind = args.kind
#     typ = args.typ
#     timeframe =args.timeframe
#     stat = args.stat
#     channels = args.channels
#     participants = args.participants
#     senders =args.senders
#
#     start = args.start
#     end = args.to
#     period = args.period
#
#     app = App(path)
#     v = app.plot()
#
#     if typ == "series":
#         v.plot_stat_count_over_time_series(kind=kind, stat=stat, channels=channels, participants=participants, start=start, end=end, period=period)
#     elif typ == "stats":
#         v.plot_stat_count_per_time_period(
#             kind=kind, timeframe=timeframe, stat=f"{stat}_count", channels=channels, participants=participants, start=start, end=end,period=period
#         )
#         pass
#     elif typ == "ranking":
#         v.plot_ranking_of_friends_by_stats(kind=kind, stat=f"{stat}_count", channels=channels, participants=participants,)
#     elif typ == "msgtype":
#         v.plot_msg_type_ratio(kind=kind, channels=channels, participants=participants, senders=senders,start=start, end=end, period=period)
#     elif typ == "convotype":
#         v.plot_convo_type_ratio(stat=stat)


# @decorators.kind_checker
# def ranking(self, kind: str, by='mc', ranking='percent', top=20):
#     analyzer = getattr(self, kind)
#     return analyzer.get_ranking_of_senders_by_convo_stats(statistic=by, top=top).get(ranking)

# def get(self,  kind: str, channels=None, senders=None, attrs=None, ):
#     analyzer = getattr(self, kind)
#     if channels or senders:
#         analyzer = analyzer.filter(channels=channels, senders=senders)
#
#     if attrs:
#         res = ''
#         for attr in attrs:  # should be one of (is_group,group_convo_map,least_contributed,most_contributed,number_of_convos_created_by_me,participants, max_channel_size,mean_channel_size,min_channel_size,)
#             value = getattr(analyzer, attr)
#             if value is None:
#                 return f'{attr} is not a valid attribute of analyzer.\n'
#             res += f'analyzer.{kind}.{attr}\t\t==> {value}'
#         return attrs
#
#     return analyzer.df.to_csv()
#
# def get_stats(self, kind=None, statistic=None, channels=None, senders=None, start=None, end=None, period=None):
#     list_of_props = utils.get_properties_of_a_class(ConversationStats)
#     if not kind:
#         return list_of_props
#     if kind not in ('private', 'group'):
#         return f'{kind} has to be either `private` or `group`!'
#     analyzer = getattr(self._analyzer, kind)
#     stats = analyzer.stats.filter(channels=channels, senders=senders,
#                                   start=start, end=end, period=period)
#     if statistic is None:
#
#         res = ''
#         for prop in list_of_props:
#             value = getattr(stats, prop)
#             if not type(value) in (str, int, float, np.float64, np.int64, list):
#                 continue
#             res += f'analyzer.{kind}.stats.{prop}\t\t\t\t==> {value}\n'
#         return res
#     return f'analyzer.{kind}.stats.{statistic}\t\t==> {getattr(stats, statistic)}'
# def get_stats_for_time_intervals(stat_getter, time_series, period):
#     data = {}
#     for i in range(len(time_series)):
#         start = time_series[i]
#         try:  # with this solution we will have data for the very last moments until datetime.now()
#             end = time_series[i + 1]
#         except IndexError:
#             end = None
#         data[start] = stat_getter.filter(
#             senders=, start=start, end=end, period=period
#         )
#     return data
# class PrivateConversationStats(ConversationStats):
#     """
#     Statistics of conversation with one or more persons.
#     """
#
#     def __init__(self, df: pd.DataFrame) -> None:
#         super().__init__(df)
#
#     def filter(self, df: pd.DataFrame = None, **kwargs:Any) -> ConversationStats:
#         if df is None:
#             df = self.df
#         df = self.get_filtered_df(df, **kwargs:Any)
#         return PrivateConversationStats(df)
#
#
# class ConversationStats(ConversationStats):
#     """
#     Statistics of conversation with one or more groups.
#     """
#
#     def __init__(self, df: pd.DataFrame) -> None:
#         super().__init__(df)
#         self.multi = self.number_of_groups > 1

# @staticmethod
# def get_filtered_df(
#         df: pd.DataFrame,
#         channel: Union[str, List[str]] = None,  # could be useful when filtering big dfs
#         subject: str = "all",
#         **kwargs,
# ) -> pd.DataFrame:
#     filter_messages = utils.CommandChainCreator()
#     filter_messages.register_command(
#         utils.filter_by_channel, column="partner", channels=channel
#     )
#     filter_messages.register_command(
#         utils.filter_for_subject, column="sender_name", senders=subject
#     )
#     filter_messages.register_command(utils.filter_by_date, **kwargs:Any)
#     return filter_messages(df)

# class PrivateMessagingAnalyzer(MessagingAnalyzer):
#     # private convo data
#     def __init__(self, data: Dict[str, Conversation]) -> None:
#         super().__init__(data)
#         self._stats = ConversationStats(self.df)
#         self._stats_per_partner = self.get_stats_per_partner()


# class GroupMessagingAnalyzer(MessagingAnalyzer):
#     # group convo data
#     def __init__(
#             self, data: Dict[str, Conversation], group_convo_map: Dict[str, List]
#     ) -> None:
#         super().__init__(data)
#         self._stats = ConversationStats(self.df)
#         self.group_convo_map = group_convo_map
#
#         self._stats_per_conversation = self.get_stats_per_conversation()
#         self._stats_per_partner = self.get_stats_per_sender()

# @property
# def number_of_convos_created_by_me(self):
#     # ok
#     return sum(
#         [stat.created_by_me for stat in self.stats_per_conversation.values()]
#     )
#
# @property
# def stats_per_conversation(self):
#     # this is stats_per_channel
#     return self._stats_per_conversation
#
# @property
# def stats_per_partner(self):
#     # this is
#     return self._stats_per_partner

# def get_stats_per_conversation(self):
#     return {
#         name: ConversationStats(convo.data)
#         for name, convo in self.data.items()
#     }
#
# def get_stats_per_partner(self) -> Dict[str, ConversationStats]:
#     stat_per_participant = {}
#     for name in self.participants:
#         stat_per_participant[name] = self.stats.filter(senders=name)
#     # looks like the following:
#     # self => whatever names where filtered (either 1 or more groups)
#     # self.stats => all time stats for the filtered names
#     # self.stats.names => should be all the real names, that are part of the/these group message(s)
#     # self.stats.filter(names=name) we only create stats for one member of the group messages(s)
#     return stat_per_participant

# class ConversationAnalyzer:
#     """
#     Analyzer for analyzing specific and/or all conversations
#
#     """
#
#     def __init__(self, conversations: Conversations) -> None:
#         self.conversations = conversations
#
#         # self.private = PrivateMessagingAnalyzer#conversations.private
#         self.private = conversations.private
#         self.groups = conversations.group
#         self.names: List[str] = list(self.private.keys())
#
#         # self.df: pd.DataFrame = self.get_df(self.private, self.group)
#         # self._stats = ConversationStats(self.df)
#
#         self.priv_df: pd.DataFrame = self.get_df(self.private)
#         self._priv_stats = PrivateConversationStats(self.priv_df)
#
#         self.group_df: pd.DataFrame = self.get_df(self.groups)
#         self._group_stats = ConversationStats(self.group_df)
#
#     def __str__(self) -> str:
#         return f"Analyzing {len(self.priv_df)} messages..."
#
#     @property
#     def priv_stats(self) -> PrivateConversationStats:
#         return self._priv_stats
#
#     @property
#     def stat_sum(self) -> pd.Series:
#         return self.priv_stats.stat_sum
#
#     @property
#     def group_stats(self) -> ConversationStats:
#         return self._group_stats
#
#     def get_stats(
#             self,
#             kind: str = "private",
#             names: str = Union[str,None],
#             subject: str = "all",
#             start: Union[str, datetime] = None,
#             end: Union[str, datetime] = None,
#             period: Union[str, datetime] = None,
#     ) -> ConversationStats:
#         if kind == "private":
#             return self.priv_stats.filter(
#                 names=names, senders=subject, start=start, end=end, period=period
#             )
#         elif kind == "group":
#             return self.group_stats.filter(
#                 names=names, senders=subject, start=start, end=end, period=period
#             )
#
#     def get_stat_count(
#             self, kind: str = "private", attribute: str = "mc", **kwargs
#     ) -> int:
#         stats = self.get_stats(kind=kind, **kwargs:Any)
#         return getattr(stats, attribute)
#
#     # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
#     def most_used_messages(self, top=20) -> pd.Series:
#         return self.priv_stats.get_most_used_messages(top)
#
#     # 5. All time: time series: dict of 'y/m/d/h : number of msgs/words/chars (also sent/got) for user/all convos'
#     def get_grouped_time_series_data(self, period="y") -> pd.DataFrame:
#         return self.priv_stats.get_grouped_time_series_data(period=period)
#
#     # 6. All time: number of messages sent/got on busiest period (by year/month/day/hour)
#     def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
#         return self.priv_stats.stat_per_period(period, statistic=statistic)
#
#     # 7. All time: Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
#     def get_ranking_of_partners_by_messages(self, statistic: str = "mc") -> Dict:
#         return self.priv_stats.get_ranking_of_partners_by_messages(statistic=statistic)
#
#     @staticmethod
#     def get_df(convos) -> pd.DataFrame:
#         return utils.stack_dfs(*[convo.data for convo in convos.values()])

# NOTE maybe needed for cli to turn date to datetime
# def year_converter(func):
#     """
#     Higher-order function that converts @year param passed to @func into numeric version.
#     @param func:
#     @return:
#     """
#
#     def wrapper(*args, **kwargs:Any):
#         if not kwargs.get('year'):
#             return func(*args, **kwargs:Any)
#         if not isinstance(kwargs.get('year'), int):
#             if kwargs.get('year').isdigit():
#                 kwargs['year'] = int(kwargs.get('year'))
#             else:
#                 print(f'Year is not a digit. Given year: {kwargs.get("year")}')
#         return func(*args, **kwargs:Any)
#
#     return wrapper
#
#
# def month_converter(func):
#     """
#     Higher-order function that converts @month param passed to @func into numeric version.
#     @param func:
#     @return:
#     """
#
#     def wrapper(*args, **kwargs:Any):
#         if not kwargs.get('month'):
#             return func(*args, **kwargs:Any)
#         if isinstance(kwargs['month'], str) and not kwargs['month'].isdigit():
#             kwargs['month'] = MONTHS.index(kwargs['month'].lower()) + 1
#         return func(*args, **kwargs:Any)
#
#     return wrapper
#
#
# def month_sorter(x):
#     return MONTHS.index(x[0])
#
#
# def lower_names(col):
#     return col.str.lower()
#
#
# def without_accent_and_whitespace(col):
#     return col.apply(replace_accents)
#
# def get_messages(*files, decode=True):
#     data = {}
#     for file in files:
#         temp = decode_text(read_json(file)) if decode else read_json(file)
#         if not data:
#             data = temp
#         elif data.get('messages') and temp.get('messages'):
#             data['messages'] += temp.get('messages')
#             if sorted(temp.keys()) != sorted(data.keys()):
#                 data = {**temp, **data}
#     return data


# class FormalParserInterface(metaclass=abc.ABCMeta):
#     @classmethod
#     def __subclasshook__(cls, subclass):
#         return (hasattr(subclass, 'load_data_source') and
#                 callable(subclass.load_data_source) and
#                 hasattr(subclass, 'extract_text') and
#                 callable(subclass.extract_text) or
#                 NotImplemented)
#
#     @abc.abstractmethod
#     def load_data_source(self, path: str, file_name: str):
#         """Load in the data set"""
#         raise NotImplementedError
#
#     @abc.abstractmethod
#     def extract_text(self, full_file_path: str):
#         """Extract text from the data set"""
#         raise NotImplementedError
# class PdfParserNew(Analyzer):
#     """Extract text from a PDF."""
#     def load_data_source(self, path: str, file_name: str) -> str:
#         """Overrides FormalParserInterface.load_data_source()"""
#         pass
#
#     def extract_text(self, full_file_path: str) -> dict:
#         """Overrides FormalParserInterface.extract_text()"""
#         pass
#
# class EmlParserNew(FormalParserInterface):
#     """Extract text from an email."""
#     def load_data_source(self, path: str, file_name: str) -> str:
#         """Overrides FormalParserInterface.load_data_source()"""
#         pass
#
#     def extract_text_from_email(self, full_file_path: str) -> dict:
#         """A method defined only in EmlParser.
#         Does not override FormalParserInterface.extract_text()
#         """
#         pass


# class ConversationAnalyzer(Analyzer):
#     # def __new__(cls, name, messages, *args, **kwargs:Any):
#     #     if messages is None:  # This deals with the case if no messages
#     #         return None
#     #     return super(ConversationAnalyzer, cls).__new__(cls, *args, **kwargs:Any)
#     def __init__(self, people):
#         super().__init__(people)
#
#
#     # def __init__(self, name, messages):
#     #     super().__init__()
#     #     self.name = name
#     #     self.df = messages
#
#     # def __str__(self):
#     #     return f'{self.name}: {list(self.df.index)}'
#     #
#     # @property
#     # def stats(self):
#     #     return self.get_stats(self.df)

# class MessagingAnalyzer(Analyzer):
#     def __init__(self, people):
#         super().__init__(people)
#         # self.names = people.names
#         # self.people = people.data
#         # self.df = self.stack_dfs()
#
#     # def stack_dfs(self):
#     #     dfs = []
#     #     for data in self.people.values():
#     #         if data.messages is not None:
#     #             dfs.append(data.messages)
#     #     return pd.concat(dfs).sort_index()
#     #
#     # def get_count(self, attribute, senders='all', start=None, end=None, period=None):
#     #     count = 0
#     #     # we have a list of names we want to iterate over
#     #     for name in self.names:
#     #         stats = self.get_conversation_stats(name=name, senders=subject, start=start, end=end, period=period)
#     #         if stats is not None:
#     #             count += getattr(stats, attribute)
#     #     return count
#     #
#     # def get_conversation_stats(self, name, senders='all', start=None, end=None, period=None):
#     #     messages = self.people.get(name).messages
#     #     analyzer = ConversationAnalyzer(name, messages)
#     #     if analyzer is None:
#     #         return None
#     #     return analyzer.get_stats(messages, senders=subject, start=start, end=end, period=period)
#     #
#     # # 1. Total count of messages/words/characters (also by year/month/day/hour)
#     # # 2. Total count of messages/words/characters sent (also by year/month/day/hour)
#     # # 3. Total count of messages/words/characters received (also by year/month)
#     # def total_number_of_(self, attribute, senders='all', **kwargs:Any):
#     #     return self.get_count(attribute=attribute, senders=subject, **kwargs:Any)
#     #
#     # # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
#     # def most_used_messages_(self, **kwargs:Any):
#     #     """
#     #     >>> s1 = pd.Series([3, 1, 2, 3, 4, 1, 1])
#     #     >>> s2 = pd.Series([3, 2, 1, 1])
#     #     >>> s1_vc = s1.value_counts()
#     #     >>> s2_vc = s2.value_counts()
#     #     LATER most used is already a problem:
#     #       - because its a series of all the unique messages/words ever used in a convo
#     #       - it contains strings like ':d', ':p' and 'xd'
#     #       - from all the convos the result of value_counts has to be cleared
#     #       and has to be truncated (that is not use the 200th most used word, only top10 let's say)
#     #       - then these series has to be merged in a way that the same string's counts are added up
#     #       - what about typos????!
#     #     """
#     #     pass
#     #
#     # # 5. Number of messages sent/got on busiest period (by year/month/day/hour)
#     # def stat_per_period(self,period, attribute, **kwargs:Any):
#     #     #  can this be used in ConvoAnalyzer?
#     #     interval_stats = self.get_time_series_data(period, **kwargs:Any)
#     #     #  attribute is one of (msg, word, char)
#     #     time_series_data = self.get_plottable_time_series_data(interval_stats, statistic=attribute)
#     #     return utils.count_stat_for_period(time_series_data, period)
#     #
#     #
#     # # 6. Time series: dict of 'year/month/day/hour : number of messages/words/characters (also sent/got) for user/all convos'
#     #
#     # # 7. Ranking of friends by messages by y/m/d/h, by different stats, by sent/got
#     # def get_ranking_of_friends_by_messages(self, attribute='mc', senders='all', start=None, end=None,
#     #                                        period=None):
#     #     #  almost the same function as get_count
#     #     count_dict = {}
#     #     for name in self.names:
#     #         stats = self.get_conversation_stats(name=name, senders=subject, start=start, end=end, period=period)
#     #         if stats is not None:
#     #             count_dict = utils.fill_dict(count_dict, name, getattr(stats, attribute))
#     #     # sort
#     #     #  put this into a func
#     #     count_dict = {key: value for key, value in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
#     #     return count_dict

# # 1. Total count of messages/words/characters (also by year/month/day/hour)
# def total_number_of_messages(self, **kwargs:Any):
#     return self.total_number_of_(attribute='mc', **kwargs:Any)
#
#
# def total_number_of_words(self, **kwargs:Any):
#     return self.total_number_of_(attribute='wc', **kwargs:Any)
#
#
# def total_number_of_characters(self, **kwargs:Any):
#     return self.total_number_of_(attribute='cc', **kwargs:Any)
#
#
# # 2. Total count of messages/words/characters sent (also by year/month/day/hour)
# def total_number_of_messages_sent(self, **kwargs:Any):
#     return self.total_number_of_(attribute='mc', senders='me', **kwargs:Any)
#
#
# def total_number_of_words_sent(self, **kwargs:Any):
#     return self.total_number_of_(attribute='wc', senders='me', **kwargs:Any)
#
#
# def total_number_of_characters_sent(self, **kwargs:Any):
#     return self.total_number_of_(attribute='cc', senders='me', **kwargs:Any)
#
#
# # 3. Total count of messages/words/characters received (also by year/month)
# def total_number_of_messages_received(self, **kwargs:Any):
#     return self.total_number_of_(attribute='mc', senders='partner', **kwargs:Any)
#
#
# def total_number_of_words_received(self, **kwargs:Any):
#     return self.total_number_of_(attribute='wc', senders='partner', **kwargs:Any)
#
#
# def total_number_of_characters_received(self, **kwargs:Any):
#     return self.total_number_of_(attribute='cc', senders='partner', **kwargs:Any)

# stats = {}
#
# for name, person in p.data.items():
#     if person.messages is None:
#         stats[person.name] = None
#         continue
#     analyzer = ConversationAnalyzer(person.name, person.messages)
#     #stats[person.name] = analyzer.stats
#     stats[person.name] = analyzer.get_stats(period='y',  senders='me', )
#     # if stats[person.name].get('message_count').get('me') > 5000:
#     #    top[person.name] = stats[person.name]
# example = stats['Dániel Nagy']
# print(example.most_used_msgs)
# print(example.most_used_words)

# print('LEN: ', len(top.keys()))
# top_all = {name: data.get('message_count').get('all') for name, data in top.items()}
# analyzer.visualize_stats(top)

# MsgAnalyzer
# @staticmethod
# def loop_over_months(data, senders='all', attribute=None):  #  generalize
#     count = 0
#     if not data:
#         print('The selected year has no data.')
#         return count
#     for stats in data.values():  # stats is the statistics for a month
#         count += getattr(stats.get(subject), attribute)
#     return count

# @staticmethod
# def get_stat_for_intervals(name, df, time_series):
#     data = {}
#     for offset, series in time_series.items():
#         data[offset] = {}
#         for i in range(len(series) - 1):  # only looping len - 1 times
#             start = series[i]
#             end = series[i + 1]  #  will we miss the last entry?
#             trimmed = df.loc[start:end]
#
#             # check if it has length
#             data[offset][start] = ConversationAnalyzer(name, trimmed) if len(trimmed.index) else None
#     return data

# @year_and_month_checker
# def get_count_for_a_person(self, stats, year=None, month=None, senders='all', attribute=None):
#     if year is None and month is None:
#         # add up all the messages count
#         return getattr(stats.get(subject), attribute)
#     elif year and not month:
#         # add up all the messages count in that year
#         return None
#         # return self.loop_over_months(stats.get('grouped').get(year), senders=subject, attribute=attribute)
#     elif year and month:
#         # add up all the messages count in that year and month
#         return None
#         # return getattr(stats.get('grouped').get(year).get(month).get(subject), attribute)
# def get_messages(self, name):
#     return self.people.get(name).messages
"""
    :
    - plan:
      - ~~see if filtering the big df works as expected~~
        - ~~filter by date, sender~~
        - ~~output should be another df~~
        - ~~output df is an input for ConvoAnalyzer~~
      - if there is a POC, decide on the data structure
        create one master df
        BUT!!!
        both has a problem of, we loose the information, whom I sent the message (is it even needed)
        - what do I need from user-specific time series:
          - timespan-specific msg/word/char count, down to year/month/day/hour level (basically the stats better filtered, not in a dict)
          - how to implement:
            - one idea would be to have time series lists like: (times = pd.date_range('2012-10-01', periods=289, freq='5min'))
                - [dt(year=2011),2012,2013, ...],
                - [dt(year=2012, month=1), dt(year=2012, month=2), ...],
                - days,
                - hours,
                then we could filter for these timespans, extract the needed lines from the df and save it to another df
                this other df would have stats
                all the dfs for all the timespans would have stats
                that we could plot
                years: 2011: stats, 2012: stats ..... and so ooooooon
          - later nice time-based graph of the above numbers
        - what do I need from global time-series:
          - same as above, but is not implemented
            - how to implement:
              - **should have** ~~OR not have~~ an intermediate data container -> that is a HUGE FUCKING df OR dict with the above data structure, that has the stats

    - implementation:
      - time series data for one person:
        - ~~have all the messages in one df for one person~~
        - ~~date should be the index, first locally,~~ but later change it from the beginning
        - ~~generate y/m/d/h timeseries~~
        - ~~split df to sub-dfs, and generate stats from them right away~~
        - ~~assign stats to  y/m/d/h timeseries entries~~
      - time series data for all people:
        - ~~stack the dfs together~~
        - sort by date
        - ~~generate y/m/d/h timeseries~~
        - split df to sub-dfs, and generate stats from them right away:
          - this would have a problem that ConvoAnalyzer is not general enough. it requires a name, that is only one person.
          -  generalize ConvoAnalzyer for this purpose (maybe use `!=`)
        - assign stats to  y/m/d/h timeseries entries

    - changes to incorportae:
      1. i want to make the indices the dates of the messages (from the very begining), investigate what would this break
      2. i want to remove date column which is used in ConversationAnalyzer. this breaks number 3.
      3. i want to omit using multiple dfs for different months sooo `stats.get('grouped')` will be no longer

"""

# def hack_around_with_filtering(self, name=None):
#     import datetime
#     if not name:
#         return
#     stats = self.get_conversation_stats(name=name).get('all')
#     df = stats.df
#     print(df.head())
#     df[(df['col1'] >= 1) & (df['col1'] <=1 )]
#     df.query('col1 <= 1 & 1 <= col1')
#     print(df[(df.sender_name == utils.ME) & (df.date.month == 12)])
#     print(df.date.month)
#     print(df.index)
#     print(df.query('20141101 < date < 20141201'))
#     print()
#     df = df.set_index(['date']).iloc[::-1]
#     print(df.index)
#     print(df)
#     print(df.loc['20141101':'20141201'])
#     print(df.loc[datetime.date(year=2014, month=11, day=1):datetime.date(year=2014, month=12, day=1)])
#     print(df.loc[datetime.datetime(year=2014, month=11, day=10, hour=12, minute=21):datetime.date(year=2014, month=12, day=1)])
#     trimmed_df =df.loc[datetime.datetime(year=2014, month=11, day=10, hour=12, minute=21):datetime.date(year=2014, month=12, day=1)]
#     print(trimmed_df)
#     print(trimmed_df[trimmed_df.sender_name == utils.ME])
# 7.


"""
- ~~basic time series would look like this:~~ MAKES NO SENSE. we have the df, use it for filtering and for stats
          - users
          |_ Teflon Musk
            |_ 2010
              |_ january
                |_ 1
                  |_ 0-1
                    |_ message 1 \\ this two
                    |_ message 2 // are in a df
                  |_ 1-2
                  |_ 2-3
                  |_ ...
                |_ 2
                |_ ...
              |_ febr
              |_ ...
            |_ 2011
            |_ 2012
            ...
"""

# utils.py
# def year_and_month_checker(func):
#     """
#     Higher-order function for checking if specified @year passed to @func is in the data dict.
#     @param func:
#     @return:
#     """
#
#     def wrapper(*args, **kwargs:Any):
#         self = args[0]
#         stats = args[1]
#         year = kwargs.get('year')
#         month = kwargs.get('month')
#
#         if year is not None and not isinstance(year, int):
#             kwargs['year'] = int(year)
#             year = kwargs.get('year')
#
#         if year is None and month is None:
#             return func(*args, **kwargs:Any)
#
#         if year and stats.get('grouped').get(year) is None:
#             # print(f"{year} is not in the data dict.")
#             return 0
#         elif year and month and stats.get('grouped').get(year).get(month) is None:
#             # print(f"{year}/{month} is not in the data dict.")
#             return 0
#         return func(*args, **kwargs:Any)
#
#     return wrapper
"""
test
now = datetime.datetime(2020, 8, 7, 20, 51, 59, 321360)
>>> now + timedelta(days=5*365)
datetime.datetime(2025, 8, 6, 20, 51, 59, 321360)
>>> now + relativedelta(years=+5)
datetime.datetime(2025, 8, 7, 20, 51, 59, 321360)

"""

# ConvoAnalyzer.py
# self.me_df = self.df[self.df.sender_name == utils.ME]
# self.partner_df = self.df[self.df.sender_name == self.name]
# self.partner_df = self.df[self.df.sender_name != utils.ME]
# self._monthly = {}

# stats = {
#     'all': ConversationStats(self.df),
#     'me': ConversationStats(self.me_df),
#     'partner': ConversationStats(self.partner_df),
#     # instead of having the dfs already cut, we should only just filter the one and only df for a user
#     # 'grouped': self.get_stats_by_month()
# }

# def get_stats_by_month(self):
#     grouped = {}
#
#
#     self.group_by_months()
#     for year in self._monthly.keys():
#         if not grouped.get(year):
#             grouped[year] = {}
#         for month in self._monthly.get(year):
#             df = self._monthly.get(year).get(month)
#             me_df = df[df.sender_name == utils.ME]
#             #partner_df = df[df.sender_name == self.name]
#             partner_df = df[df.sender_name != utils.ME]
#             if not grouped.get(year).get(month):
#                 grouped.get(year)[month] = {}
#                 grouped.get(year)[month]['all'] = ConversationStats(df)
#                 grouped.get(year)[month]['me'] = ConversationStats(me_df)
#                 grouped.get(year)[month]['partner'] = ConversationStats(partner_df)
#     return grouped
#
# def group_by_months(self):
#     # I could just simply filter pandas df (where df.date.year == year && df.date.month == month)
#     indices = self.get_indices_at_new_month(self.df)
#     dfs = self.split_df_at_indices(self.df, indices)
#
#     for df in dfs:
#         date = df['date'][0]  # datetime.strptime(df['date'][0], '%Y-%m-%d')
#         if not self._monthly.get(date.year):
#             self._monthly[date.year] = {}
#         self._monthly[date.year][date.month] = df
#
# @staticmethod
# def get_indices_at_new_month(df):
#     indices = []
#     last_month = -1
#
#     for i, date in enumerate(df['date']):
#         # date = datetime.strptime(timestamp, '%Y-%m-%d')
#         if date.month != last_month:
#             indices.append(i)
#             last_month = date.month
#     return indices
#
# @staticmethod
# def split_df_at_indices(df, indices):
#     indices += [len(df)]
#     return [df.iloc[indices[n]:indices[n + 1]].reset_index(drop=True) for n in range(len(indices) - 1)]

'''
        # me_wc, me_unique_wc = self.wc(self.me_df)
        # p_wc, p_unique_wc = self.wc(self.partner_df)
        #
        # me_cc = self.character_count(self.me_df)
        # p_cc = self.character_count(self.partner_df)
        #
        # return {
        #     'message_count': {
        #         'me': len(self.me_df),
        #         'partner': len(self.partner_df),
        #         'all': len(self.me_df) + len(self.partner_df),
        #     },
        #     'wc': {
        #         'me': me_wc,
        #         'partner': p_wc,
        #         'all': me_wc + p_wc,
        #     },
        #     'character_count': {
        #         'me': me_cc,
        #         'partner': p_cc,
        #         'all': me_cc + p_cc,
        #     },
        # }

    # def get_stat_for(self,df):
    #    return ConversationStats(df)

    # def visualize_stats(self, stats):
    #     print(stats)
    #     # print(sorted(stats.items(), key=operator.itemgetter(1), reverse=True))
    #     stats_sorted = self.sort_stats(stats)
    #     for name, stat in stats_sorted.items():
    #         print(f'{name}:\n {stat}\n')
    #
    # @staticmethod
    # def sort_stats(stats):
    #     stats_sorted = {}
    #     name_wc = {}
    #
    #     for name, stat in stats.items():
    #         name_wc[name] = stat.get('wc').get('all')
    #     sorted_wc = dict(sorted(name_wc.items(), key=operator.itemgetter(1), reverse=True))
    #
    #     for name, wc in sorted_wc.items():
    #         stats_sorted[name] = stats[name]
    #
    #     return stats_sorted
        # self.tokens = None  

    # def messages_count(self):
    #     me = len(self.me_df)
    #     partner = len(self.partner_df)
    #     return me, partner
    #
    # @staticmethod
    # def get_words(df):
    #     token_list = df.content.str.lower().str.split()
    #     words = []
    #     for tokens in token_list:
    #         # print(tokens)
    #         if not isinstance(tokens, list):
    #             print('WARNING! Not a list!')
    #             continue  
    #         for token in tokens:
    #             words.append(token)
    #     return words
    #
    # def wc(self, df):
    #     words = self.get_words(df)
    #     return len(words), len(set(words))

    # def character_count(self, df):
    #     words = self.get_words(df)
    #     cc = 0
    #
    #     for word in words:
    #         cc += len(word)
    #     return cc
    @property
    def words_me(self):
        return self.get_words(self.me_df)

    @property
    def words_partner(self):
        return self.get_words(self.partner_df)
    def unique_wc(self, party=None):
        if not party:
            return self.stats.get('')


    def most_used_words(self):
        pass

    def number_of_messages_sent(self):
        pass

    def number_of_messages_sent_by_party(self):
        pass

    def number_of_messages_sent_by_time_interval(self):
        pass

    def wc_per_message(self):
        pass

    def character_count_per_message(self):
        pass
'''
'''
        # messages = 0
        # # we have a dict of `name<string> : person <obj>`
        # # we want to iterate over the dict
        # for name in self.names:
        #     # person = self.people.get(name)
        #     stats = self.get_conversation_stats(name=name)
        #     # if not year and not month
        #     if not year and not month:
        #         # add up all the messages count
        #         messages += stats.get('all').mc
        #     # if year and not month
        #     elif year and not month:
        #         def get_mc(stat):
        #             return stat.mc
        #
        #         # add up all the messages count in that year
        #         messages += self.loop_over_months(stats.get(year), func=get_mc)
        #
        #     # if year and month
        #     elif year and month:
        #         # add up all the messages count in that year and month
        #         messages += stats.get(year).get(month)
        # def get_mc(stat):
        #     return stat.mc
'''
# @period_checker
# def generate_time_series(offset=None, start=None, end=None, period=None):
#     start = start or datetime(year=2009, month=10, day=2, hour=0)
#     end = end or datetime.now()
#     time_series = {
#         'y': pd.date_range(start=start, end=end, freq='YS'),  #  does not include 2009
#         'm': pd.date_range(start=start, end=end, freq='1MS'),  #  does not include october
#         'd': pd.date_range(start=start, end=end, freq='1D'),  #  does not include 2. ?! not sure if it is true
#         #  put this back after dev phase is over
#         # 'h': pd.date_range(start=start, end=end, freq='1H'), #  hour should only be run ONCE
#     }
#     if offset is not None and offset in ('y', 'm', 'd', 'h'):
#         return time_series[period]
#     return time_series


# PLOTTER
# could be interesting to see which months (jan, feb, jun, jul, aug..)/days/hours are the busiest
# def plot_time_bar_data(sent_data,received_data, name):
#     const_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#
#     trace1 = go.Bar(
#         x=list(dict(sorted(dict(Counter(messages_days['sent'])).items(), key=lambda x: const_days.index(x[0]))).keys()),
#         y=list(dict(sorted(dict(Counter(messages_days['sent'])).items(), key=lambda x: const_days.index(x[0]))).values()),
#         name='Sent by ' + receiver.split()[0],
#         marker=dict(
#             color='rgb(239,86,117)',
#         )
#     )
#     trace2 = go.Bar(
#         x=list(dict(sorted(dict(Counter(messages_days['received'])).items(), key=lambda x: const_days.index(x[0]))).keys()),
#         y=list(
#             dict(sorted(dict(Counter(messages_days['received'])).items(), key=lambda x: const_days.index(x[0]))).values()),
#         name='Sent by ' + sender.split()[0],
#         marker=dict(
#             color='rgb(59,89,152)',
#         )
#     )
#     data = [trace1, trace2]
#     layout = go.Layout(
#         barmode='stack',
#         title=go.layout.Title(
#             text='Number of Messages per Day',
#             xref='paper',
#             x=0
#         ),
#         xaxis=go.layout.XAxis(
#             title=go.layout.xaxis.Title(
#                 text='Day'
#             )
#         ),
#         yaxis=go.layout.YAxis(
#             title=go.layout.yaxis.Title(
#                 text='Number of Messages'
#             )
#         )
#     )
#
#     fig = go.Figure(data=data, layout=layout)
#     pio.write_image(fig, save_path + '/Day-Wise-Comparison.png')

# ##Plotting Month Data
#
# const_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#                 'November', 'December']
#
# trace1 = go.Bar(
#     x=list(dict(sorted(dict(Counter(messages_months['sent'])).items(), key=lambda x: const_months.index(x[0]))).keys()),
#     y=list(
#         dict(sorted(dict(Counter(messages_months['sent'])).items(), key=lambda x: const_months.index(x[0]))).values()),
#     name='Sent by ' + receiver.split()[0],
#     marker=dict(
#         color='rgb(239,86,117)',
#     )
# )
# trace2 = go.Bar(
#     x=list(dict(
#         sorted(dict(Counter(messages_months['received'])).items(), key=lambda x: const_months.index(x[0]))).keys()),
#     y=list(dict(
#         sorted(dict(Counter(messages_months['received'])).items(), key=lambda x: const_months.index(x[0]))).values()),
#     name='Sent by ' + sender.split()[0],
#     marker=dict(
#         color='rgb(59,89,152)',
#     )
# )
#
# data = [trace1, trace2]
# layout = go.Layout(
#     barmode='stack',
#     title=go.layout.Title(
#         text='Number of Messages per Month',
#         xref='paper',
#         x=0
#     ),
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='Month'
#         )
#     ),
#     yaxis=go.layout.YAxis(
#         title=go.layout.yaxis.Title(
#             text='Number of Messages'
#         )
#     )
# )
#
# fig = go.Figure(data=data, layout=layout)
# pio.write_image(fig, save_path + '/Month-Wise-Comparison.png')

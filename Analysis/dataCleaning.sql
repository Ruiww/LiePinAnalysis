#提取salary，获得min-max-average salary
#新建列
ALTER TABLE DATA ADD (
min_salary FLOAT(10),
max_salary FLOAT(10),
average_salary FLOAT(10)
) ;
#when `salary` like '%面议%',min/max/average=0
UPDATE DATA SET `min_salary`=0, `max_salary`=0, `average_salary`=0
WHERE  `salary` LIKE '%面议%' ;
#salary不是面谈时，salary格式'min-max万'
#min_salary=min
UPDATE DATA SET `min_salary`= SUBSTRING_INDEX(`salary`,'-',1)
WHERE `salary` LIKE '%-%万%';
#max_Salary=max
UPDATE DATA SET `max_salary`= (SUBSTRING(SUBSTRING_INDEX(`salary`,'万',1),LOCATE('-',SUBSTRING_INDEX(`salary`,'万',1))+1))
WHERE `salary` LIKE '%-%万%';
#average_salary = (min+max)/2
UPDATE DATA SET `average_salary`= (min_salary+max_salary)/2
WHERE `salary` LIKE '%-%万%';

#整理position，XX-XX或XX
ALTER TABLE DATA ADD (
position1 VARCHAR(255),
position2 VARCHAR(255)
);
UPDATE DATA SET position1 = position
WHERE position NOT LIKE '%-%';
UPDATE DATA SET position2 = 'null'
WHERE position NOT LIKE '%-%';
UPDATE DATA SET position1 = SUBSTRING_INDEX(`position`,'-',1)
WHERE position LIKE '%-%';
UPDATE DATA SET position2 = SUBSTRING(`position`,LOCATE('-',`position`)+1)
WHERE position LIKE '%-%';

#发布时间pubtime：str->date to newfield：pubdate
SELECT @y :=LEFT(data.`PubTime`,4) FROM `data`;
SELECT @m :=mid(pubtime,6,2) FROM `data`;
SELECT @d :=mid(pubtime,9,2) FROM `data`;
UPDATE `data` SET `pubdate`=str_to_Date(
concat(@y,'-',@m,'-',@d),'%Y-%m-%d');

#整理qualification
#学历
SELECT substring_index(qualification,' ',1)
FROM `data`;
UPDATE TABLE `data` SET education = 
substring_index(qualification,' ',1)
#工作经验
UPDATE `data` SET 
`workexperience` = substring(substring_index(qualification,' ',2),char_length(substring_index(qualification,' ',1))+2) ;
#年龄要求
UPDATE `DATA` SET 
`age` = substring_index(qualification,' ',-1) ;
#工作语言
UPDATE `data` SET workLANGUAGE = 
mid(
qualification,
char_length(substring_index(qualification,' ',2))+2,
char_length(substring(`qualification`,char_length(substring_index(qualification,' ',2))+2))-char_length(`age`)-1
);

#找出comsize内容实际为address的，将其内容赋予comAddr并删除comsize内的内容
UPDATE DATA SET `comAddress`=`companySize`
WHERE (`companySize` NOT LIKE '%-%人%' AND companySize NOT LIKE '%人以上') ;
UPDATE DATA SET `companySize`=' '
WHERE (`companySize` NOT LIKE '%-%人%' AND companySize NOT LIKE '%人以上') ;

#填充空缺内容
#industry_detail为空时，用industry的内容填充
UPDATE DATA SET industry_detail = industry 
WHERE `industry_detail`=' ' ;
#addr内容为空时用position内容填充
UPDATE DATA SET `comAddress` = `position`
WHERE `comAddress`=' ' ;
#size内容为空时，填写'null'
UPDATE DATA SET `companySize` = 'null'
WHERE `companySize`=' ' ;
#tag_list内容为空时，填写'null'
UPDATE DATA SET `tag_list` = 'null'
WHERE `tag_list`=' ' ;
#description内容为空时，填写'null'
UPDATE DATA SET `description` = 'null'
WHERE `description`=' ' ;

#查询用于分析的数据
SELECT jobtitle,company,min_salary,max_salary,average_salary,pdate,
tag_list,description,industry,companysize,comaddress,position1,
education,workexperience,worklanguage,age,is_end
FROM `data`
WHERE (
jobtitle LIKE '%数据%分析%' 
OR jobtitle LIKE'%大数据%' 
OR jobtitle LIKE '%大数据%' 
OR jobtitle LIKE '%数据%运营%'
OR jobtitle LIKE '%data%'
)
AND (is_end = 0);
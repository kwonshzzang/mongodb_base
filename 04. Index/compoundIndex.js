use sample_training;

show collections

db.zips.findOne()

db.zips.getIndexes()

db.zips.find(
    {
        state: 'LA',
        pop: {
            $gte: 40000
        }
    }
).sort({city: 1})


db.zips.find(
    {
        state: 'LA',
        pop: {
            $gte: 40000
        }
    }
).sort({city: 1}).explain('executionStats')

// executionStats: {
//     executionSuccess: true,
//     nReturned: 13,
//     executionTimeMillis: 24,
//     totalKeysExamined: 0,
//     totalDocsExamined: 29470,


db.zips.createIndex({state: 1})

db.zips.getIndexes()

db.zips.find(
    {
        state: 'LA',
        pop: {
            $gte: 40000
        }
    }
).sort({city: 1}).explain('executionStats')

// executionStats: {
//     executionSuccess: true,
//     nReturned: 13,
//     executionTimeMillis: 1,
//     totalKeysExamined: 469,
//     totalDocsExamined: 469,

db.zips.createIndex({state: 1, city: 1, pop: 1})

db.zips.getIndexes()

db.zips.find(
    {
        state: 'LA',
        pop: {
            $gte: 40000
        }
    }
).sort({city: 1}).explain('executionStats')

// executionStats: {
//     executionSuccess: true,
//     nReturned: 13,
//     executionTimeMillis: 3,
//     totalKeysExamined: 419,
//     totalDocsExamined: 13,

db.zips.find(
    {
        state: 'LA',
        pop: {
            $gte: 40000
        }
    }, 
    {
        _id: 0,
        state: 1,
        pop: 1,
        city: 1
    }
).sort({city: 1}).explain('executionStats')

// executionStats: {
//     executionSuccess: true,
//     nReturned: 13,
//     executionTimeMillis: 2,
//     totalKeysExamined: 419,
//     totalDocsExamined: 0,
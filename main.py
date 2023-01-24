from Models.Population import Population
from Utilities import Logger
import csv

logger = Logger(debug=True)

POPULATION_SIZE = 1000
GENERATIONS = 1000

uuid = 0
def next_uuid():
    global uuid
    uuid += 1
    return uuid

population = Population(POPULATION_SIZE)

output_file_name = "./OutputFiles/output.csv"
database_file_name = "./OutputFiles/database.csv"
    
with open(output_file_name, 'w') as output_file: 
    headers = ['N', 'Signal Effort', 'Trust', 'Signal', 'Value', 'Arbitrary']
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(headers)
with open(database_file_name, 'w') as database_file: 
    headers = ["UUID", "Generation", "Sex", "Quality", "Effort", "Signal", "Value", "Trust", "Area", "Children", "Successors"]
    csv_writer = csv.writer(database_file)
    csv_writer.writerow(headers)

for i in range(GENERATIONS):
    if not logger.show_debugging:
        logger.display_progress("Evolving: ", i, GENERATIONS)
    previous_generation = population.evolve()
    with open(database_file_name, 'a') as database_file:
        csv_writer = csv.writer(database_file)
        max_children_male = 0
        max_children_female = 0
        for male in previous_generation["males"]:
            if male.num_children > max_children_male:
                max_children_male = male.num_children
            row = [next_uuid(), i, 'M', male.quality, male.signaling_effort, male.signal, male.value, male.trust, (male.signal*male.value), male.num_children, male.num_surviving_children]
            csv_writer.writerow(row)
        for female in previous_generation["females"]:
            if female.num_children > max_children_female:
                max_children_female = female.num_children
            row = [next_uuid(), i, 'F', female.quality, female.signaling_effort, female.signal, female.value, female.trust, (female.signal*female.value), female.num_children, female.num_surviving_children]
            csv_writer.writerow(row)
    buffer = " "*len("Generation " + str(i))
    logger.debug("Generation", i, "max_children_male:  ", max_children_male)
    logger.debug(buffer, "max_children_female:", max_children_female)

    if logger.show_debugging:
        average_quality = 0
        average_signaling_effort = 0
        average_trust = 0
        average_perceived_signal = 0
        average_value_after_signaling = 0
        average_arbitrary = 0
        for male in population.males:
            average_quality += male.quality
            average_signaling_effort += male.signaling_effort
            average_trust += male.trust
            average_perceived_signal += male.signal
            average_value_after_signaling += male.value
            average_arbitrary += male.value
        for female in population.females:
            average_quality += female.quality
            average_signaling_effort += female.signaling_effort
            average_trust += female.trust
            average_arbitrary += female.trust
        average_quality /= POPULATION_SIZE
        average_signaling_effort /= POPULATION_SIZE
        average_trust /= POPULATION_SIZE
        average_perceived_signal /= len(population.males)
        average_value_after_signaling /= len(population.males)
        average_arbitrary /= POPULATION_SIZE

        with open(output_file_name, 'a') as output_file: 
            row = [i+1, average_signaling_effort, average_trust, average_perceived_signal, average_value_after_signaling, average_arbitrary]
            csv_writer = csv.writer(output_file) 
            csv_writer.writerow(row)

        logger.debug(buffer, " average_quality               ", str(round(100*average_quality)), '%', delimiter='')
        logger.debug(buffer, " average_signaling_effort      ", str(round(100*average_signaling_effort)), '%', delimiter='')
        logger.debug(buffer, " average_trust                 ", str(round(100*average_trust)), '%', delimiter='')
        logger.debug(buffer, " average_perceived_signal      ", str(round(100*average_perceived_signal)), '%', delimiter='')
        logger.debug(buffer, " average_value_after_signaling ", str(round(100*average_value_after_signaling)), '%', delimiter='')
        logger.debug(buffer, " average_arbitrary             ", str(round(100*average_arbitrary)), '%', delimiter='')

if not logger.show_debugging:
    logger.display_progress("Evolving: ", GENERATIONS, GENERATIONS, final=True)

    average_quality = 0
    average_signaling_effort = 0
    average_trust = 0
    for male in population.males:
        average_quality += male.quality
        average_signaling_effort += male.signaling_effort
        average_trust += male.trust
    for female in population.females:
        average_quality += female.quality
        average_signaling_effort += female.signaling_effort
        average_trust += female.trust
    average_quality /= POPULATION_SIZE
    average_signaling_effort /= POPULATION_SIZE
    average_trust /= POPULATION_SIZE

    logger.info(buffer, " average_quality          ", str(round(100*average_quality)), '%', delimiter='')
    logger.info(buffer, " average_signaling_effort ", str(round(100*average_signaling_effort)), '%', delimiter='')
    logger.info(buffer, " average_trust            ", str(round(100*average_trust)), '%', delimiter='')

logger.debug("Done!")
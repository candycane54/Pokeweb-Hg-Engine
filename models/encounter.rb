class Encounter < Pokenarc


	def self.get_all
		@@narc_name = "encounters"
		data = super
		expand_encounter_info(data)

	end

	def self.get_data file_name, type="readable"
		@@narc_name = "encounters"
		super
	end


	def self.write_data data, batch=false
		@@narc_name = "encounters"
		@@upcases = []
		super
	end

	def self.get_max_level id
		enc =  get_data("#{$rom_name}/json/encounters/#{id}.json")
		max = 0
		(0..11).each do |n|
			if enc["spring_grass_doubles_slot_#{n}_max_level"] > max
				max = enc["spring_grass_doubles_slot_#{n}_max_level"]
			end
		end

		(0..11).each do |n|
			if enc["spring_grass_slot_#{n}_max_level"] > max
				max = enc["spring_grass_slot_#{n}_max_level"]
			end
		end

		return max if max != 0

		(0..4).each do |n|
			if enc["spring_surf_slot_#{n}_max_level"] > max
				max = enc["spring_surf_slot_#{n}_max_level"]
			end
		end

		max
	end

	def self.copy_season_to_all id, copied_season
		enc_path = "#{$rom_name}/json/encounters/#{id}.json"
		enc_data = get_data(enc_path, "all")
		
		enc = enc_data.clone
		

		["readable", "raw"].each do |type|
			enc_data[type].each do |k, v|
				(["spring", "summer", "fall", "winter"] - [copied_season]).each do |season|
					if k.include? season
						enc[type][k] = enc[type][k.gsub(season, copied_season)]
					end
				end
			end
		end

		File.open(enc_path, "w") { |f| f.write enc.to_json }
		"200 OK"
	end


	def self.expand_encounter_info(encounter_data)
		encounter_count = encounter_data.length

		encounter_data.each_with_index do |enc, i|
			wilds = []
			

			grass_fields.each do |enc_type|
				(0..11).each do |n|
					wilds << enc["#{enc_type}_#{n}_species_id"].gsub(/[^0-9A-Za-z\-]/, '').name_titleize
				end
			end
			extra_fields.each_with_index do |enc_type, j|
				(0..extra_field_counts[j] - 1).each do |n|
					wilds << enc["#{enc_type}_#{n}_species_id"].gsub(/[^0-9A-Za-z\-]/, '').name_titleize
				end
			end

			encounter_data[i]["wilds"] = wilds.reject(&:empty?).uniq
			encounter_data[i]["wilds"].delete("-----")
		end
		encounter_data
	end

	def self.seasons
		["spring", "summer", "fall", "winter"]
	end

	def self.grass_fields
		["morning", "day", "night"]
	end

	def self.water_fields
		["surf", "surf_special", "super_rod" , "super_rod_special"]
	end

	def self.extra_fields
		["surf", "rock_smash", "old_rod", "good_rod", "super_rod", "hoenn", "sinnoh"]
	end

	def self.extra_field_counts
		[5,2,5,5,5,2,2]
	end

	def self.grass_percent_for(n)
		[20,20,10,10,10,10,5,5,4,4,1,1][n]
	end

	def self.extra_percent_for(n)
		[60, 30, 5, 4, 1][n]
	end

	def self.output_documentation
	end
end

